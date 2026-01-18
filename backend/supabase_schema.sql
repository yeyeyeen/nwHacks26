-- ===========================================
-- Supabase Database Schema for GitHub OAuth
-- ===========================================
-- Run this in Supabase SQL Editor to create the required tables

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ===========================================
-- C1. Users Table
-- ===========================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- ===========================================
-- C2. GitHub Accounts Table
-- ===========================================
CREATE TABLE IF NOT EXISTS github_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    github_id BIGINT UNIQUE NOT NULL,
    github_login VARCHAR(255) NOT NULL,
    access_token TEXT NOT NULL,  -- Encrypted using Fernet
    scope TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_github_accounts_user_id ON github_accounts(user_id);
CREATE INDEX IF NOT EXISTS idx_github_accounts_github_id ON github_accounts(github_id);
CREATE INDEX IF NOT EXISTS idx_github_accounts_github_login ON github_accounts(github_login);

-- ===========================================
-- Row Level Security (RLS) Policies
-- ===========================================
-- Enable RLS on tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE github_accounts ENABLE ROW LEVEL SECURITY;

-- Policy: Allow service role full access (for backend operations)
-- Note: Supabase service role bypasses RLS by default

-- Policy: Users can only read their own data (if using authenticated users)
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (true);  -- Adjust based on your auth needs

CREATE POLICY "GitHub accounts are readable" ON github_accounts
    FOR SELECT USING (true);  -- Adjust based on your auth needs

-- For insert/update, service role handles this
CREATE POLICY "Service can insert users" ON users
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Service can update users" ON users
    FOR UPDATE USING (true);

CREATE POLICY "Service can insert github_accounts" ON github_accounts
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Service can update github_accounts" ON github_accounts
    FOR UPDATE USING (true);

-- ===========================================
-- Trigger to update updated_at timestamp
-- ===========================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_github_accounts_updated_at
    BEFORE UPDATE ON github_accounts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

