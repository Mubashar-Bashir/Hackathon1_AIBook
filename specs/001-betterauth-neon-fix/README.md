# BetterAuth Neon Database Integration - Demo Users

This directory contains the specification and tools for fixing BetterAuth connection issues with Neon database and creating demo users for testing.

## Files

- `spec.md` - Feature specification for BetterAuth Neon database integration
- `demo-users-script.py` - Script to create 10 demo users for sign-in testing
- `requirements.txt` - Dependencies for the demo user script
- `checklists/requirements.md` - Specification quality checklist

## Creating Demo Users

To create 10 demo users for testing the sign-in functionality:

### 1. Install Dependencies

```bash
pip install asyncpg
```

### 2. Set Environment Variable

Make sure your `NEON_DATABASE_URL` environment variable is set:

```bash
export NEON_DATABASE_URL="your_neon_database_connection_string"
```

### 3. Run the Script

```bash
python demo-users-script.py
```

### 4. Expected Output

The script will create 10 demo users with the following format:
- Email: `username@example.com`
- Password: Randomly generated secure password
- Experience Level: Rotated between "beginner", "intermediate", and "expert"

The script will display all the credentials for testing purposes.

## Testing Sign-In

Once the demo users are created, you can test the sign-in functionality using:
- The web interface at the login page
- API testing tools like curl or Postman
- Direct API calls to the authentication endpoints

## Database Schema

The script will create the following table if it doesn't exist:
- `users` table with columns: id, email, name, username, password, experience_level, created_at, updated_at, is_active

## Troubleshooting

If you encounter issues:
1. Verify the `NEON_DATABASE_URL` is correctly set
2. Check that your Neon database is accessible
3. Ensure you have the necessary permissions to create tables and insert data
4. Confirm that the asyncpg library is properly installed