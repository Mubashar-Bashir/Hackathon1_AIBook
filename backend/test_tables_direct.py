"""Direct test to create tables and check if they exist in the same connection."""

import asyncio
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import text

# Add the backend directory to the path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

async def test_tables_creation_direct():
    """Test creating tables and checking existence in the same connection."""
    from src.utils.database import async_engine, Base
    from src.models.user import User
    from src.models.session import Session

    print("Creating tables in a single connection...")

    async with async_engine.begin() as conn:
        # Create all tables
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully")

        # Check if users table exists in the same connection
        result = await conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'users'
            );
        """))
        users_exist = result.scalar()
        print(f"Users table exists: {users_exist}")

        # Check if sessions table exists in the same connection
        result = await conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'sessions'
            );
        """))
        sessions_exist = result.scalar()
        print(f"Sessions table exists: {sessions_exist}")

        # List all tables in the same connection
        result = await conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """))
        tables = [row[0] for row in result.fetchall()]
        print(f"All tables in public schema: {tables}")

        return users_exist, sessions_exist

async def main():
    users_exist, sessions_exist = await test_tables_creation_direct()

    print(f"\nSummary: Users table exists: {users_exist}, Sessions table exists: {sessions_exist}")

    if users_exist and sessions_exist:
        print("SUCCESS: Tables were created and are visible!")
    else:
        print("FAILURE: Tables were not created or not visible.")

if __name__ == "__main__":
    asyncio.run(main())