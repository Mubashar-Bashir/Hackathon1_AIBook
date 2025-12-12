-- Migration script for creating the accounts table
-- This table stores external authentication provider information

CREATE TABLE IF NOT EXISTS accounts (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    provider_id VARCHAR(255) NOT NULL,
    provider_name VARCHAR(50) NOT NULL,
    provider_account_id VARCHAR(255) NOT NULL,
    access_token TEXT,
    refresh_token TEXT,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_accounts_user_id ON accounts(user_id);
CREATE INDEX IF NOT EXISTS idx_accounts_provider_name ON accounts(provider_name);
CREATE INDEX IF NOT EXISTS idx_accounts_provider_account_id ON accounts(provider_account_id);
CREATE INDEX IF NOT EXISTS idx_accounts_provider_combination ON accounts(provider_name, provider_account_id);

-- Create unique constraint to prevent duplicate provider accounts for same user
ALTER TABLE accounts ADD CONSTRAINT uk_accounts_provider_user UNIQUE (provider_name, provider_account_id, user_id);

-- Create trigger to update the updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_accounts_updated_at
    BEFORE UPDATE ON accounts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();