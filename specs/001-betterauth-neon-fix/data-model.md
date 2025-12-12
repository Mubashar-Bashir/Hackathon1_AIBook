# Data Model: BetterAuth Neon Database Integration

## Overview
This document describes the data structures and entities for the BetterAuth authentication system integrated with Neon PostgreSQL database for the AIBook project.

## Entities

### User
A registered user of the AIBook platform with authentication credentials and profile information.

**Attributes**:
- id: String - Unique identifier for the user (UUID format)
- email: String - User's email address (unique, required)
- name: String - User's full name (optional)
- username: String - Unique username for the user (optional)
- password_hash: String - Securely hashed password (required)
- experience_level: String - User's experience level (beginner, intermediate, expert)
- is_active: Boolean - Whether the account is active (default: true)
- is_verified: Boolean - Whether the email is verified (default: false)
- created_at: DateTime - Timestamp when user was created
- updated_at: DateTime - Timestamp when user was last updated
- last_login: DateTime - Timestamp of last login (nullable)

**Validation Rules**:
- email must be a valid email format
- email must be unique across all users
- password_hash must be present and properly formatted
- experience_level must be one of: "beginner", "intermediate", "expert"
- created_at and updated_at are automatically managed

### Session
An active authentication session for a user.

**Attributes**:
- id: String - Unique session identifier (UUID format)
- user_id: String - Reference to the associated user
- session_token: String - Secure session token (unique, required)
- expires_at: DateTime - Expiration timestamp for the session
- created_at: DateTime - Timestamp when session was created
- updated_at: DateTime - Timestamp when session was last updated
- ip_address: String - IP address from which session was created (optional)
- user_agent: String - Browser/device information (optional)

**Validation Rules**:
- user_id must reference an existing user
- session_token must be unique across all sessions
- expires_at must be in the future
- Automatically cleaned up when expired

### Account
Account information for linking external authentication providers (if needed).

**Attributes**:
- id: String - Unique account identifier (UUID format)
- user_id: String - Reference to the associated user
- provider_id: String - Identifier from the external provider
- provider_name: String - Name of the external provider (e.g., "google", "github")
- provider_account_id: String - Account ID from the external provider
- access_token: String - Access token for the external provider (encrypted)
- refresh_token: String - Refresh token for the external provider (encrypted)
- expires_at: DateTime - Expiration timestamp for tokens (nullable)
- created_at: DateTime - Timestamp when account was linked
- updated_at: DateTime - Timestamp when account was last updated

**Validation Rules**:
- user_id must reference an existing user
- Combination of provider_name and provider_account_id must be unique
- Access tokens should be encrypted when stored

### Verification Token
Temporary token for account verification or password reset operations.

**Attributes**:
- id: String - Unique identifier for the token (UUID format)
- user_id: String - Reference to the associated user
- token: String - Secure random token string (unique, required)
- token_type: String - Type of verification (email_verification, password_reset)
- expires_at: DateTime - Expiration timestamp for the token
- used_at: DateTime - Timestamp when token was used (nullable)
- created_at: DateTime - Timestamp when token was created

**Validation Rules**:
- user_id must reference an existing user
- token must be unique across all verification tokens
- token_type must be one of: "email_verification", "password_reset"
- expires_at must be in the future
- Cannot be used after expiration or after being used once

## Relationships

### User to Session
- One-to-Many: A user can have multiple active sessions
- Foreign Key: sessions.user_id references users.id
- Cascade: Sessions are deleted when user is deleted

### User to Account
- One-to-Many: A user can link multiple external accounts
- Foreign Key: accounts.user_id references users.id
- Cascade: Accounts are deleted when user is deleted

### User to Verification Token
- One-to-Many: A user can have multiple verification tokens (for different purposes)
- Foreign Key: verification_tokens.user_id references users.id
- Cascade: Tokens are deleted when user is deleted

## Database Indexes

### Required Indexes:
- users.email: Unique index for fast email lookups during authentication
- sessions.session_token: Unique index for fast session validation
- verification_tokens.token: Unique index for fast token validation
- users.username: Unique index if username is used for login (optional)

### Performance Indexes:
- sessions.expires_at: Index for efficient cleanup of expired sessions
- verification_tokens.expires_at: Index for efficient cleanup of expired tokens
- users.created_at: Index for user analytics and reporting

## Constraints

### Data Integrity:
- Email uniqueness is enforced at the database level
- Session token uniqueness is enforced at the database level
- Referential integrity is maintained with foreign key constraints
- Password hashes are stored with proper length constraints

### Security:
- Sensitive fields (tokens, passwords) are properly secured
- Automatic cleanup of expired data through scheduled jobs or database features
- Audit trail for authentication-related operations (via updated_at timestamps)