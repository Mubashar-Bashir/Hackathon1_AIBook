"""Test to check what's in the metadata."""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

async def test_metadata():
    """Test what's in the metadata."""
    from src.utils.database import Base
    from src.models.user import User
    from src.models.session import Session

    print("Inspecting Base metadata...")
    print(f"Tables in Base.metadata: {list(Base.metadata.tables.keys())}")

    # Import the models to register them with Base
    print("User class:", User)
    print("Session class:", Session)
    print("User table name:", getattr(User, '__tablename__', 'No __tablename__'))
    print("Session table name:", getattr(Session, '__tablename__', 'No __tablename__'))

    print(f"After importing, tables in Base.metadata: {list(Base.metadata.tables.keys())}")

    # Let's manually create the tables by accessing them
    user_table = User.__table__
    session_table = Session.__table__

    print(f"User table: {user_table}")
    print(f"Session table: {session_table}")

    print(f"After accessing tables, tables in Base.metadata: {list(Base.metadata.tables.keys())}")

async def main():
    await test_metadata()

if __name__ == "__main__":
    asyncio.run(main())