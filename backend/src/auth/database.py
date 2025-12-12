"""
Database migration runner for AIBook authentication system
"""
import asyncio
import asyncpg
import os
from typing import List, Dict, Any
from pathlib import Path


class MigrationRunner:
    def __init__(self, database_url: str = None):
        self.database_url = database_url or os.getenv("NEON_DATABASE_URL")
        if not self.database_url:
            raise ValueError("Database URL is required. Set NEON_DATABASE_URL environment variable.")

    async def run_migrations(self) -> Dict[str, Any]:
        """
        Run all pending database migrations
        """
        results = {
            "success": True,
            "migrations_run": [],
            "errors": []
        }

        try:
            # Connect to the database
            conn = await asyncpg.connect(dsn=self.database_url)

            try:
                # Create migrations tracking table if it doesn't exist
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS schema_migrations (
                        id SERIAL PRIMARY KEY,
                        migration_name VARCHAR(255) UNIQUE NOT NULL,
                        executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Get list of already executed migrations
                executed_migrations = await conn.fetch(
                    "SELECT migration_name FROM schema_migrations ORDER BY executed_at"
                )
                executed_migration_names = {row['migration_name'] for row in executed_migrations}

                # Get all migration files from the migrations directory
                migrations_dir = Path(__file__).parent.parent.parent / "migrations"
                if not migrations_dir.exists():
                    results["errors"].append(f"Migrations directory does not exist: {migrations_dir}")
                    results["success"] = False
                    return results

                migration_files = sorted([f for f in migrations_dir.glob("*.sql")])

                # Execute each migration that hasn't been run yet
                for migration_file in migration_files:
                    migration_name = migration_file.name

                    if migration_name in executed_migration_names:
                        continue  # Skip already executed migrations

                    try:
                        # Read the migration SQL
                        with open(migration_file, 'r') as f:
                            sql_content = f.read()

                        # Execute the migration in a transaction
                        async with conn.transaction():
                            await conn.execute(sql_content)
                            await conn.execute(
                                "INSERT INTO schema_migrations (migration_name) VALUES ($1)",
                                migration_name
                            )

                        results["migrations_run"].append(migration_name)
                        print(f"✓ Executed migration: {migration_name}")

                    except Exception as e:
                        error_msg = f"Failed to execute migration {migration_name}: {str(e)}"
                        results["errors"].append(error_msg)
                        results["success"] = False
                        print(f"✗ {error_msg}")
                        break  # Stop on first error to maintain consistency

            finally:
                await conn.close()

        except Exception as e:
            error_msg = f"Failed to connect to database: {str(e)}"
            results["errors"].append(error_msg)
            results["success"] = False
            print(f"✗ {error_msg}")

        return results

    async def check_pending_migrations(self) -> List[str]:
        """
        Check which migrations are pending (not yet executed)
        """
        pending_migrations = []

        try:
            conn = await asyncpg.connect(dsn=self.database_url)

            try:
                # Get list of already executed migrations
                executed_migrations = await conn.fetch(
                    "SELECT migration_name FROM schema_migrations ORDER BY executed_at"
                )
                executed_migration_names = {row['migration_name'] for row in executed_migrations}

                # Get all migration files from the migrations directory
                migrations_dir = Path(__file__).parent.parent.parent / "migrations"
                if migrations_dir.exists():
                    migration_files = sorted([f for f in migrations_dir.glob("*.sql")])

                    # Find pending migrations
                    for migration_file in migration_files:
                        migration_name = migration_file.name
                        if migration_name not in executed_migration_names:
                            pending_migrations.append(migration_name)

            finally:
                await conn.close()

        except Exception as e:
            print(f"Error checking pending migrations: {e}")

        return pending_migrations

    async def create_database_tables(self) -> Dict[str, Any]:
        """
        Create all required database tables for the authentication system
        """
        # This is an alternative approach that directly executes our migration files
        return await self.run_migrations()


# Convenience function to run migrations
async def run_auth_migrations() -> Dict[str, Any]:
    """
    Convenience function to run authentication database migrations
    """
    runner = MigrationRunner()
    return await runner.run_migrations()


# Example usage
if __name__ == "__main__":
    async def main():
        runner = MigrationRunner()

        print("Checking for pending migrations...")
        pending = await runner.check_pending_migrations()
        if pending:
            print(f"Found {len(pending)} pending migrations: {pending}")
        else:
            print("No pending migrations found")

        print("\nRunning migrations...")
        results = await runner.run_migrations()

        print(f"\nMigration Results:")
        print(f"Success: {results['success']}")
        print(f"Migrations run: {results['migrations_run']}")
        if results['errors']:
            print(f"Errors: {results['errors']}")

    # Run the migration process
    asyncio.run(main())