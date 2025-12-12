# Quickstart: BetterAuth Neon Database Integration

## Overview
This guide provides instructions for setting up and using the BetterAuth authentication system with Neon PostgreSQL database for the AIBook project. This includes user registration, authentication, and database integration.

## Prerequisites
- Node.js 18+ installed
- Python 3.11+ installed
- Neon PostgreSQL database instance
- Access to the AIBook project repository

## Environment Setup

### 1. Database Configuration
1. Create a Neon PostgreSQL database instance
2. Copy the connection string from your Neon dashboard
3. Add to your `.env` file:
   ```
   NEON_DATABASE_URL=your_neon_database_connection_string
   ```

### 2. Install Dependencies
```bash
cd backend
pip install -r requirements.txt  # Python dependencies
cd ../book
npm install                     # Frontend dependencies
```

## Database Initialization

### 1. Run Database Migrations
The BetterAuth Neon integration includes automatic schema creation for all required tables:

```bash
cd backend
python -m scripts.setup_auth_db
```

This will create the following tables:
- `users` - User account information
- `sessions` - Active authentication sessions
- `verification_tokens` - Temporary tokens for email verification/password reset

### 2. Verify Database Tables
```bash
python -m scripts.verify_auth_tables
```

## API Endpoints

### Authentication Endpoints

#### Register New User
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "SecurePassword123!",
  "experience_level": "beginner"
}
```

**Response**:
```json
{
  "success": true,
  "user": {
    "id": "user-uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "experience_level": "beginner"
  },
  "session_token": "session-token-string"
}
```

#### Login
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response**:
```json
{
  "success": true,
  "user": {
    "id": "user-uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "experience_level": "beginner"
  },
  "session_token": "session-token-string"
}
```

#### Get Current User
```
GET /api/auth/me
Authorization: Bearer session-token-string
```

**Response**:
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "experience_level": "beginner",
  "created_at": "2025-01-01T00:00:00Z"
}
```

#### Logout
```
POST /api/auth/logout
Authorization: Bearer session-token-string
```

**Response**:
```json
{
  "success": true,
  "message": "Successfully logged out"
}
```

#### Forgot Password
```
POST /api/auth/forgot-password
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Password reset email sent if account exists"
}
```

#### Reset Password
```
POST /api/auth/reset-password
Content-Type: application/json

{
  "token": "verification-token-from-email",
  "new_password": "NewSecurePassword123!"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Password reset successfully"
}
```

## Frontend Integration

### 1. Using Authentication in Components
The authentication system is integrated into the Docusaurus frontend through React context:

```javascript
import { useAuth } from '../contexts/AuthContext';

function MyComponent() {
  const { user, isAuthenticated, login, logout, register } = useAuth();

  if (!isAuthenticated) {
    return <LoginForm onLogin={login} />;
  }

  return (
    <div>
      <h1>Welcome, {user.name}!</h1>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

### 2. Protected Routes
Use the `RequireAuth` wrapper to protect routes that require authentication:

```javascript
import RequireAuth from '../components/RequireAuth';

function ProtectedPage() {
  return (
    <RequireAuth>
      <div>Protected content here</div>
    </RequireAuth>
  );
}
```

## Testing Authentication

### 1. Unit Tests
Run the authentication unit tests:
```bash
cd backend
pytest tests/auth/test_auth.py
```

### 2. Integration Tests
Test the complete authentication flow:
```bash
cd backend
pytest tests/auth/test_database.py
```

### 3. Manual Testing
1. Register a new user using the API endpoint
2. Verify the user exists in the Neon database
3. Login with the registered user credentials
4. Access protected endpoints with the session token
5. Logout and verify session invalidation

## Troubleshooting

### Common Issues

#### Database Connection Issues
- Verify NEON_DATABASE_URL is correctly set in your environment
- Check that your Neon database is active and accessible
- Ensure your IP address is allowed in Neon's connection settings

#### Authentication Failing
- Confirm password hashing is working correctly
- Check that session tokens are being properly created and validated
- Verify that user account is active (is_active = true)

#### Migration Problems
- Run the migration script again if tables are missing
- Check for any constraint violations in the data model
- Verify that the database user has appropriate permissions

## Security Considerations

- Passwords are securely hashed using industry-standard algorithms
- Session tokens are randomly generated and securely stored
- Rate limiting is implemented to prevent brute force attacks
- All authentication endpoints use HTTPS in production
- Input validation is performed on all user inputs

## Next Steps

1. Integrate user preferences and personalization features
2. Implement additional authentication providers if needed
3. Add multi-factor authentication for enhanced security
4. Set up monitoring and logging for authentication events