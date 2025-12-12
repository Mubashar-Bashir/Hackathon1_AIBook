#!/usr/bin/env python3
"""
Verification script to check if demo users were created successfully
"""

import asyncio
import asyncpg
import os

async def verify_demo_users():
    """Verify that the demo users were created in the database."""
    print("Verifying demo users in database...")

    # Connect to database
    database_url = os.getenv("NEON_DATABASE_URL")
    if not database_url:
        raise ValueError("NEON_DATABASE_URL environment variable not set")

    conn = await asyncpg.connect(database_url)

    try:
        # Count total users
        user_count = await conn.fetchval("SELECT COUNT(*) FROM users;")
        print(f"Total users in database: {user_count}")

        # Get demo users specifically
        demo_users = await conn.fetch(
            "SELECT id, email, name, experience_level, created_at FROM users WHERE id LIKE 'demo_user_%' ORDER BY id;"
        )

        print(f"\nFound {len(demo_users)} demo users:")
        print("-" * 80)
        print(f"{'ID':<15} {'Email':<25} {'Name':<20} {'Level':<12} {'Created'}")
        print("-" * 80)

        for user in demo_users:
            print(f"{user['id']:<15} {user['email']:<25} {user['name']:<20} {user['experience_level']:<12} {user['created_at']}")

        print("-" * 80)

        if len(demo_users) >= 10:
            print(f"\n✅ SUCCESS: Found {len(demo_users)} demo users (expected 10)")
            print("Demo users are ready for sign-in testing!")
        else:
            print(f"\n⚠️  WARNING: Found {len(demo_users)} demo users (expected 10)")

    except Exception as e:
        print(f"❌ Error verifying users: {str(e)}")
    finally:
        await conn.close()

if __name__ == "__main__":
    print("BetterAuth Demo User Verification")
    print("=" * 50)
    asyncio.run(verify_demo_users())