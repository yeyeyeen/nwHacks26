# GitHub OAuth Integration Guide

This document explains how to set up and use the GitHub OAuth integration in this backend.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [GitHub OAuth App Setup](#github-oauth-app-setup)
3. [Supabase Database Setup](#supabase-database-setup)
4. [Environment Configuration](#environment-configuration)
5. [API Endpoints](#api-endpoints)
6. [Token Encryption](#token-encryption)
7. [Testing the Flow](#testing-the-flow)

---

## Prerequisites

1. **GitHub Account** - Required to create an OAuth App
2. **Supabase Account** - Free tier available at [supabase.com](https://supabase.com)
3. **Python 3.8+** - With the required dependencies installed

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## GitHub OAuth App Setup

### Step 1: Register a GitHub OAuth App

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click **"New OAuth App"**
3. Fill in the application details:
   - **Application name**: Your app name (e.g., "My Feedback App")
   - **Homepage URL**: `http://localhost:8000` (for development)
   - **Authorization callback URL**: `http://localhost:8000/auth/github/callback`
4. Click **"Register application"**

### Step 2: Get Your Credentials

After registration, you'll see:
- **Client ID**: Copy this value
- **Client Secret**: Click "Generate a new client secret" and copy it

⚠️ **Important**: Store these securely. Never commit them to version control.

---

## Supabase Database Setup

### Step 1: Create a Supabase Project

1. Go to [Supabase](https://supabase.com) and sign in
2. Click **"New Project"**
3. Fill in the project details and wait for setup

### Step 2: Run the Database Migration

1. Go to **SQL Editor** in your Supabase dashboard
2. Copy the contents of `supabase_schema.sql`
3. Run the SQL to create the required tables:
   - `users` - Stores user accounts
   - `github_accounts` - Stores GitHub OAuth connections

### Step 3: Get Your Supabase Credentials

From your project settings:
- **SUPABASE_URL**: Settings > API > Project URL
- **SUPABASE_KEY**: Settings > API > Project API keys > `anon` key (or `service_role` for backend)

---

## Environment Configuration

### Step 1: Generate Encryption Key

Run this command to generate a Fernet encryption key:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### Step 2: Create .env File

Copy `.env.example` to `.env` and fill in all values:

```bash
cp .env.example .env
```

Required environment variables:
```env
# GitHub OAuth
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GITHUB_REDIRECT_URI=http://localhost:8000/auth/github/callback

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key

# Token Encryption
TOKEN_ENCRYPTION_KEY=your-generated-fernet-key
```

---

## API Endpoints

### 1. Login Endpoint

**GET** `/auth/github/login`

Redirects the user to GitHub's OAuth authorization page.

**Example:**
```
http://localhost:8000/auth/github/login
```

**Response:** Redirects to GitHub with the following parameters:
- `client_id`: Your GitHub Client ID
- `scope`: `repo,user`
- `redirect_uri`: Your callback URL

---

### 2. Callback Endpoint

**GET** `/auth/github/callback?code=...`

Handles the OAuth callback from GitHub. This endpoint:
1. Exchanges the authorization code for an access token
2. Fetches the user's GitHub profile
3. Creates or updates the user in the database
4. Returns authentication result

**Query Parameters:**
- `code` (required): The authorization code from GitHub

**Success Response (200):**
```json
{
  "success": true,
  "message": "Successfully authenticated with GitHub",
  "user": {
    "github_id": 12345678,
    "github_login": "username",
    "email": "user@example.com",
    "name": "User Name",
    "avatar_url": "https://avatars.githubusercontent.com/u/12345678"
  },
  "github_account": {
    "id": "uuid-here",
    "user_id": "user-uuid",
    "github_login": "username",
    "scope": "repo,user"
  }
}
```

**Error Responses:**
- `400`: Invalid authorization code
- `500`: Server configuration error

---

### 3. Status Endpoint

**GET** `/auth/github/status`

Check if GitHub OAuth is properly configured.

**Response:**
```json
{
  "configured": true,
  "client_id_set": true,
  "client_secret_set": true,
  "redirect_uri": "http://localhost:8000/auth/github/callback"
}
```

---

## Token Encryption

All GitHub access tokens are encrypted before storage using **Fernet symmetric encryption** (part of the `cryptography` library).

### How It Works

1. **Encryption**: When a user authenticates, the access token is encrypted using `encrypt_token(token)` before being stored in the database.

2. **Decryption**: When you need to use the token (e.g., to make GitHub API calls), use `decrypt_token(encrypted_token)` to get the original token.

### Usage in Code

```python
from app.utils.encryption import encrypt_token, decrypt_token

# Encrypt a token before storage
encrypted = encrypt_token("ghp_xxxxxxxxxxxx")

# Decrypt when needed
original = decrypt_token(encrypted)
```

### Retrieving Tokens

```python
from app.services.supabase_db import get_decrypted_access_token

# Get decrypted token for a user
token = get_decrypted_access_token(github_id=12345678)
```

---

## Testing the Flow

### Step 1: Start the Server

```bash
python main.py
```

Or with uvicorn (with auto-reload for development):
```bash
uvicorn main:app --reload
```

### Step 2: Check Configuration

Visit: `http://localhost:8000/auth/github/status`

Verify all values are `true`.

### Step 3: Test Login Flow

1. Open your browser and go to: `http://localhost:8000/auth/github/login`
2. You'll be redirected to GitHub
3. Authorize the application
4. You'll be redirected back with authentication details

### Step 4: Verify Database

Check your Supabase dashboard:
- `users` table should have a new entry
- `github_accounts` table should have the OAuth connection with encrypted token

---

## Testing Without a Frontend

You can test all the GitHub OAuth endpoints without a frontend using the following methods:

### Method 1: Using curl

#### Test 1: Check Configuration Status
```bash
curl http://localhost:8000/auth/github/status
```

Expected response:
```json
{
  "configured": true,
  "client_id_set": true,
  "client_secret_set": true,
  "redirect_uri": "http://localhost:8000/auth/github/callback"
}
```

#### Test 2: Get the OAuth Login URL
```bash
curl -v http://localhost:8000/auth/github/login 2>&1 | grep -i location
```

This will show the redirect URL. Copy and paste it into your browser.

### Method 2: Using the Browser

1. **Start the server:**
   ```bash
   python main.py
   ```

2. **Open the login URL in your browser:**
   ```
   http://localhost:8000/auth/github/login
   ```

3. **Authorize on GitHub** - You'll be redirected to GitHub to authorize

4. **View the callback response** - After authorization, you'll be redirected back and see the JSON response in your browser:
   ```json
   {
     "success": true,
     "message": "Successfully authenticated with GitHub",
     "user": {
       "github_id": 12345678,
       "github_login": "your-username",
       "email": "your@email.com",
       ...
     },
     "github_account": {
       "id": "uuid",
       "user_id": "user-uuid",
       ...
     }
   }
   ```

### Method 3: Using HTTPie

```bash
# Check status
http GET http://localhost:8000/auth/github/status

# Follow redirects to see login URL
http --follow GET http://localhost:8000/auth/github/login
```

### Method 4: Using Python Requests

```python
import requests

# Check configuration status
response = requests.get("http://localhost:8000/auth/github/status")
print(response.json())

# Get login redirect URL (don't follow redirects)
response = requests.get("http://localhost:8000/auth/github/login", allow_redirects=False)
print(f"Login URL: {response.headers['Location']}")
```

### Method 5: Using FastAPI Interactive Docs

1. Start the server: `python main.py`
2. Open: `http://localhost:8000/docs`
3. You'll see all endpoints with interactive testing UI
4. Click on any endpoint to expand and test it

### Testing the Complete OAuth Flow Manually

If you need to test the callback endpoint directly (e.g., for debugging), you'll need a valid authorization code from GitHub. Here's how:

1. **Get the authorization URL:**
   ```bash
   curl -s http://localhost:8000/auth/github/login 2>&1 | grep -oP '(?<=Location: ).*'
   ```

2. **Open that URL in your browser and authorize**

3. **Copy the `code` parameter from the redirect URL** (shown in browser address bar)

4. **Test the callback endpoint:**
   ```bash
   curl "http://localhost:8000/auth/github/callback?code=YOUR_CODE_HERE"
   ```

   ⚠️ Note: Authorization codes are single-use and expire quickly!

### Checking the Logs

The application logs detailed information about each step. Watch the terminal where the server is running to see:

```
=== GitHub OAuth Login initiated ===
Redirecting to GitHub OAuth authorization
  Authorization URL: https://github.com/login/oauth/authorize
  Scopes: repo,user
  Redirect URI: http://localhost:8000/auth/github/callback

=== GitHub OAuth Callback received ===
  Authorization code: abc123...
Step 1: Exchanging authorization code for access token...
✓ Successfully exchanged code for access token
Step 2: Fetching GitHub user profile...
✓ Fetched GitHub profile for user: username
Step 3: Creating/updating user in database...
=== Upserting GitHub account for: username (github_id: 12345678) ===
✓ User authenticated successfully: username
=== GitHub OAuth flow completed successfully ===
```

### Testing Database Operations

After a successful OAuth flow, verify the data in Supabase:

1. Go to your Supabase dashboard
2. Click on **Table Editor**
3. Check the `users` table for new entries
4. Check the `github_accounts` table for OAuth connections

You can also query using the Supabase SQL Editor:
```sql
-- View all users
SELECT * FROM users ORDER BY created_at DESC;

-- View all GitHub accounts (token is encrypted)
SELECT id, user_id, github_id, github_login, scope, created_at 
FROM github_accounts 
ORDER BY created_at DESC;
```

---

## Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| email | VARCHAR(255) | User email (nullable) |
| created_at | TIMESTAMP | Creation timestamp |

### GitHub Accounts Table
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Foreign key to users |
| github_id | BIGINT | GitHub user ID (unique) |
| github_login | VARCHAR(255) | GitHub username |
| access_token | TEXT | Encrypted OAuth token |
| scope | TEXT | OAuth scopes granted |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

---

## Security Considerations

1. **Never commit secrets**: Keep `.env` in `.gitignore`
2. **Use HTTPS in production**: Update callback URL for production
3. **Token encryption**: All tokens are encrypted at rest
4. **Scope limitations**: Only request necessary GitHub scopes
5. **Token rotation**: Consider implementing token refresh mechanisms

---

## Troubleshooting

### "GitHub OAuth is not configured"
- Verify `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` are set in `.env`

### "Failed to exchange code for token"
- Check that your callback URL matches exactly
- Verify client secret is correct

### "TOKEN_ENCRYPTION_KEY not configured"
- Generate a new key using the command in Step 1 of Environment Configuration

### Database connection errors
- Verify Supabase URL and key are correct
- Ensure the SQL schema has been run

