#!/usr/bin/env python3
"""
Demo User Generator for BetterAuth Neon Database Integration
This script creates 10 demo users for testing sign-in functionality.
"""

import asyncio
import hashlib
import secrets
from datetime import datetime, timedelta
import asyncpg
import os
from typing import List, Dict, Any

# Sample names for generating realistic demo users
FIRST_NAMES = [
    "Alex", "Taylor", "Jordan", "Morgan", "Casey", "Riley", "Quinn", "Avery",
    "Peyton", "Dakota", "Jamie", "Skyler", "Reese", "Emerson", "Finley",
    "Hayden", "Rowan", "Sawyer", "Kendall", "Parker"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
]

EXPERIENCE_LEVELS = ["beginner", "intermediate", "expert"]

async def connect_to_database():
    """Connect to the Neon database using environment variables."""
    database_url = os.getenv("NEON_DATABASE_URL")
    if not database_url:
        raise ValueError("NEON_DATABASE_URL environment variable not set")

    print(f"Connecting to database...")
    conn = await asyncpg.connect(database_url)
    return conn

def generate_secure_password():
    """Generate a secure random password for demo users."""
    # Create a strong password with mixed case, numbers, and symbols
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for _ in range(12))
    return password

def hash_password(password: str) -> str:
    """Hash password using SHA-256 (for demonstration - in production, use bcrypt or similar)."""
    return hashlib.sha256(password.encode()).hexdigest()

async def create_demo_users(conn) -> List[Dict[str, Any]]:
    """Create 10 demo users with realistic data."""
    print("Creating 10 demo users...")

    demo_users = []

    for i in range(10):
        first_name = FIRST_NAMES[i % len(FIRST_NAMES)]
        last_name = LAST_NAMES[i % len(LAST_NAMES)]
        username = f"{first_name.lower()}{last_name.lower()}{i+1}"
        email = f"{username}@example.com"
        password = generate_secure_password()
        hashed_password = hash_password(password)
        experience_level = EXPERIENCE_LEVELS[i % len(EXPERIENCE_LEVELS)]

        user_data = {
            'id': f"demo_user_{i+1:02d}",
            'email': email,
            'name': f"{first_name} {last_name}",
            'username': username,
            'password': hashed_password,
            'experience_level': experience_level,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_active': True,
            'password_plaintext': password  # Store temporarily for testing purposes
        }

        demo_users.append(user_data)
        print(f"  - {email} (password: {password})")

    return demo_users

async def insert_users_into_database(conn, users: List[Dict[str, Any]]):
    """Insert demo users into the users table."""
    print("Inserting users into database...")

    # Create the users table if it doesn't exist
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        username TEXT,
        password TEXT NOT NULL,
        experience_level TEXT DEFAULT 'beginner',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE,
        session_token TEXT
    );
    """

    await conn.execute(create_table_sql)

    # Insert users
    insert_sql = """
    INSERT INTO users (
        id, email, name, username, password, experience_level,
        created_at, updated_at, is_active
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
    ON CONFLICT (email) DO UPDATE SET
        name = EXCLUDED.name,
        username = EXCLUDED.username,
        password = EXCLUDED.password,
        experience_level = EXCLUDED.experience_level,
        updated_at = EXCLUDED.updated_at,
        is_active = EXCLUDED.is_active;
    """

    for user in users:
        await conn.execute(
            insert_sql,
            user['id'], user['email'], user['name'], user['username'],
            user['password'], user['experience_level'], user['created_at'],
            user['updated_at'], user['is_active']
        )

    print(f"Successfully inserted {len(users)} demo users into the database.")

async def main():
    """Main function to create demo users."""
    print("=" * 60)
    print("BetterAuth Demo User Generator")
    print("=" * 60)

    try:
        # Connect to database
        conn = await connect_to_database()
        print("✓ Connected to database successfully")

        # Create demo users
        demo_users = await create_demo_users(conn)

        # Insert users into database
        await insert_users_into_database(conn, demo_users)

        print("\n" + "=" * 60)
        print("Demo Users Created Successfully!")
        print("=" * 60)
        print("\nDemo User Credentials for Testing:")
        print("-" * 40)

        for i, user in enumerate(demo_users, 1):
            print(f"User {i:2d}: {user['email']} / {user['password_plaintext']}")

        print("-" * 40)
        print(f"\nTotal: {len(demo_users)} demo users created and stored in the database.")
        print("These users can now be used for sign-in testing.")

        # Close connection
        await conn.close()

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print("\n✅ Demo user creation completed successfully!")
    else:
        print("\n❌ Demo user creation failed!")
        exit(1)