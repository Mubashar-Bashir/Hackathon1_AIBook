"""Simple test to check if tables exist in the database."""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

async def test_tables_exist():
    """Test if the tables exist in the database."""
    from sqlalchemy import text
    from src.utils.database import async_engine

    print("Checking if tables exist in the database...")

    async with async_engine.connect() as conn:
        # Check if users table exists
        result = await conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'users'
            );
        """))
        users_exist = result.scalar()
        print(f"Users table exists: {users_exist}")

        # Check if sessions table exists
        result = await conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'sessions'
            );
        """))
        sessions_exist = result.scalar()
        print(f"Sessions table exists: {sessions_exist}")

        # List all tables
        result = await conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """))
        tables = [row[0] for row in result.fetchall()]
        print(f"All tables in public schema: {tables}")

        return users_exist, sessions_exist

async def main():
    users_exist, sessions_exist = await test_tables_exist()

    if not users_exist or not sessions_exist:
        print("Tables don't exist. Creating them now...")
        from src.utils.database import init_db
        await init_db()
        print("Tables created. Re-checking...")
        await test_tables_exist()
    else:
        print("Tables already exist.")

if __name__ == "__main__":
    asyncio.run(main())