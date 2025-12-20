# Authentication API Documentation

## Overview
This document describes the authentication API endpoints for the AIBook platform. The authentication system provides user registration, login, profile management, and secure session handling.

## Base URL
All authentication endpoints are prefixed with `/api/auth`

## Authentication Methods
- Most endpoints require a valid session token in the Authorization header
- Format: `Authorization: Bearer <session_token>`

## Endpoints

### POST /api/auth/register
Register a new user account.

#### Request
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "SecurePassword123!",
  "experience_level": "beginner"
}
```

#### Request Parameters
- `email` (string, required): User's email address (5-100 characters)
- `name` (string, required): User's full name (1-100 characters)
- `password` (string, required): User's password (min 8 characters)
- `experience_level` (string, required): User's experience level ('beginner', 'intermediate', or 'expert')

#### Response (200 OK)
```json
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "name": "John Doe",
  "experience_level": "beginner",
  "session_token": "session-token-string",
  "created_at": "2023-12-13T10:30:00Z"
}
```

#### Error Responses
- `400 Bad Request`: Invalid registration parameters
- `409 Conflict`: User already exists
- `500 Internal Server Error`: Server error during registration

---

### POST /api/auth/login
Authenticate a user and return a session token.

#### Request
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

#### Request Parameters
- `email` (string, required): User's email address
- `password` (string, required): User's password

#### Response (200 OK)
```json
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "name": "John Doe",
  "experience_level": "beginner",
  "session_token": "session-token-string",
  "created_at": "2023-12-13T10:30:00Z"
}
```

#### Error Responses
- `400 Bad Request`: Invalid login parameters
- `401 Unauthorized`: Invalid credentials
- `500 Internal Server Error`: Server error during login

---

### GET /api/auth/profile
Get the authenticated user's profile information.

#### Headers
- `Authorization: Bearer <session_token>` (required)

#### Response (200 OK)
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "name": "John Doe",
  "username": "johndoe",
  "experience_level": "beginner",
  "created_at": "2023-12-13T10:30:00Z",
  "updated_at": "2023-12-13T10:30:00Z"
}
```

#### Error Responses
- `401 Unauthorized`: Missing or invalid authorization header
- `404 Not Found`: User not found
- `500 Internal Server Error`: Server error retrieving profile

---

### PUT /api/auth/profile
Update the authenticated user's profile information.

#### Headers
- `Authorization: Bearer <session_token>` (required)

#### Request
```json
{
  "name": "Updated Name",
  "username": "updated_username",
  "experience_level": "intermediate"
}
```

#### Response (200 OK)
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "name": "Updated Name",
  "username": "updated_username",
  "experience_level": "intermediate",
  "created_at": "2023-12-13T10:30:00Z",
  "updated_at": "2023-12-13T11:00:00Z"
}
```

#### Error Responses
- `400 Bad Request`: Invalid update parameters
- `401 Unauthorized`: Missing or invalid authorization header
- `404 Not Found`: User not found
- `500 Internal Server Error`: Server error updating profile

---

### POST /api/auth/logout
End the current user session.

#### Headers
- `Authorization: Bearer <session_token>` (required)

#### Response (200 OK)
```json
{
  "success": true,
  "message": "Successfully logged out"
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or expired session
- `500 Internal Server Error`: Server error during logout

---

### GET /api/auth/me
Retrieves information about the currently authenticated user (alias for /profile).

#### Headers
- `Authorization: Bearer <session_token>` (required)

#### Response (200 OK)
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "name": "John Doe",
  "username": "johndoe",
  "experience_level": "beginner",
  "created_at": "2023-12-13T10:30:00Z",
  "updated_at": "2023-12-13T10:30:00Z"
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or expired session
- `500 Internal Server Error`: Server error retrieving user info

---

### POST /api/auth/forgot-password
Initiates password reset process by sending reset email.

#### Request
```json
{
  "email": "user@example.com"
}
```

#### Request Parameters
- `email` (string, required): User's email address

#### Response (200 OK)
```json
{
  "success": true,
  "message": "If an account exists with this email, a password reset link has been sent"
}
```

#### Error Responses
- `400 Bad Request`: Invalid email format
- `500 Internal Server Error`: Server error during password reset request

---

### POST /api/auth/reset-password
Resets user password using verification token.

#### Request
```json
{
  "token": "verification-token",
  "new_password": "NewSecurePassword123!"
}
```

#### Request Parameters
- `token` (string, required): Verification token received via email
- `new_password` (string, required): New password (min 8 characters)

#### Response (200 OK)
```json
{
  "success": true,
  "message": "Password reset successfully"
}
```

#### Error Responses
- `400 Bad Request`: Invalid token or password
- `401 Unauthorized`: Invalid or expired token
- `500 Internal Server Error`: Server error during password reset

## Security Considerations

1. **Password Requirements**:
   - Minimum 8 characters
   - Should contain a mix of letters, numbers, and special characters

2. **Session Management**:
   - Session tokens are securely generated using `secrets.token_urlsafe(32)`
   - Sessions expire after 1 week by default
   - Sessions are invalidated on logout

3. **Rate Limiting**:
   - The system includes protections against brute force attacks
   - Multiple failed login attempts may result in temporary account lockout

4. **Data Validation**:
   - All input is validated both at the API and service layer
   - Email format validation is enforced
   - Experience level values are restricted to predefined options

## Error Handling

The API follows standard HTTP status codes:
- `200`: Success
- `400`: Client error (bad request, validation error)
- `401`: Unauthorized (invalid/missing credentials)
- `404`: Resource not found
- `409`: Conflict (e.g., duplicate email during registration)
- `500`: Server error

All error responses include a descriptive message in the response body.