-- Migration script for creating additional indexes and constraints for performance optimization

-- Additional indexes for the users table (if not already created in users_table.sql)
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_users_is_verified ON users(is_verified);
CREATE INDEX IF NOT EXISTS idx_users_last_login ON users(last_login);

-- Additional indexes for the sessions table (if not already created in sessions_table.sql)
CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON sessions(created_at);

-- Additional indexes for the accounts table (if not already created in accounts_table.sql)
CREATE INDEX IF NOT EXISTS idx_accounts_created_at ON accounts(created_at);

-- Additional indexes for the verification_tokens table (if not already created in verification_tokens_table.sql)
CREATE INDEX IF NOT EXISTS idx_verification_tokens_used_at ON verification_tokens(used_at);

-- Add foreign key constraints (if not already defined)
-- Note: These assume the referenced tables exist

-- Add constraint to ensure experience_level is valid
ALTER TABLE users ADD CONSTRAINT chk_experience_level CHECK (experience_level IN ('beginner', 'intermediate', 'expert'));

-- Add constraint to ensure provider_name is valid
ALTER TABLE accounts ADD CONSTRAINT chk_provider_name CHECK (provider_name IN ('google', 'github', 'facebook', 'twitter', 'apple', 'microsoft'));

-- Create partial indexes for better performance on commonly filtered columns
CREATE INDEX IF NOT EXISTS idx_users_active ON users(id) WHERE is_active = TRUE;
CREATE INDEX IF NOT EXISTS idx_sessions_active ON sessions(id, expires_at) WHERE expires_at > CURRENT_TIMESTAMP;
CREATE INDEX IF NOT EXISTS idx_verification_tokens_unused ON verification_tokens(id) WHERE used_at IS NULL AND expires_at > CURRENT_TIMESTAMP;

-- Create a composite index for common user lookups
CREATE INDEX IF NOT EXISTS idx_users_email_active ON users(email, is_active) WHERE is_active = TRUE;