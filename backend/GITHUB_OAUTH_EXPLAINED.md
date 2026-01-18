# GitHub OAuth Flow - How It Works

## Overview

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Frontend │────▶│ Backend  │────▶│  GitHub  │────▶│ Supabase │
│  (User)  │◀────│   API    │◀────│   OAuth  │     │    DB    │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
```

## Step-by-Step Flow

### Step 1: User Clicks "Login with GitHub"
```
Frontend: Opens http://localhost:8000/auth/github/login
```

### Step 2: Backend Redirects to GitHub
```
Backend redirects to:
https://github.com/login/oauth/authorize
  ?client_id=Ov23liPJPTcdKRDZHWBI
  &scope=repo,user
  &redirect_uri=http://localhost:8000/auth/github/callback
```

### Step 3: User Authorizes on GitHub
- User sees GitHub's authorization page
- User clicks "Authorize"
- GitHub redirects back with a temporary `code`

### Step 4: Backend Exchanges Code for Token
```
GitHub redirects to:
http://localhost:8000/auth/github/callback?code=abc123xyz

Backend makes POST to GitHub:
POST https://github.com/login/oauth/access_token
{
  "client_id": "...",
  "client_secret": "...",
  "code": "abc123xyz"
}

GitHub returns:
{
  "access_token": "gho_xxxxxxxxxxxx",
  "scope": "repo,user",
  "token_type": "bearer"
}
```

### Step 5: Backend Fetches User Profile
```
GET https://api.github.com/user
Authorization: Bearer gho_xxxxxxxxxxxx

Returns:
{
  "id": 12345678,
  "login": "username",
  "email": "user@example.com",
  ...
}
```

### Step 6: Backend Saves to Database
```
1. Create/find user in `users` table
2. Encrypt the access_token using Fernet
3. Save to `github_accounts` table:
   - github_id: 12345678
   - github_login: "username"
   - access_token: <encrypted>
   - scope: "repo,user"
```

### Step 7: Backend Returns Response to Frontend
```json
{
  "success": true,
  "message": "Successfully authenticated with GitHub",
  "user": {
    "github_id": 12345678,
    "github_login": "username",
    "email": "user@example.com"
  },
  "github_account": {
    "id": "uuid-here",
    "user_id": "user-uuid"
  }
}
```

---

## How Tokens Are Saved

### In the Database (Supabase)

```sql
-- users table
| id (UUID)                            | email              | created_at |
|--------------------------------------|--------------------|------------|
| 550e8400-e29b-41d4-a716-446655440000 | user@example.com   | 2026-01-17 |

-- github_accounts table
| id       | user_id  | github_id | github_login | access_token (ENCRYPTED) | scope     |
|----------|----------|-----------|--------------|--------------------------|-----------|
| uuid-123 | uuid-000 | 12345678  | username     | gAAAAABh...encrypted...  | repo,user |
```

### Token Encryption

The access token is **never stored in plain text**. It's encrypted using Fernet symmetric encryption:

```python
# When saving (in upsert_github_account):
encrypted_token = encrypt_token("gho_xxxxxxxxxxxx")
# Result: "gAAAAABh..." (encrypted string)

# When retrieving (to make GitHub API calls):
from app.services.supabase_db import get_decrypted_access_token
token = get_decrypted_access_token(github_id=12345678)
# Result: "gho_xxxxxxxxxxxx" (original token)
```

---

## How to Use the Saved Token

### Example: Fetch User's Repositories

```python
# In a new endpoint, retrieve the token and use it:
from app.services.supabase_db import get_decrypted_access_token
import httpx

async def get_user_repos(github_id: int):
    # Get the saved token from database
    token = get_decrypted_access_token(github_id)
    
    if not token:
        raise Exception("User not authenticated")
    
    # Use token to call GitHub API
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user/repos",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            }
        )
        return response.json()
```

---

## Frontend Integration

### Option 1: Redirect-Based Flow (Simple)

```javascript
// Frontend: Redirect user to login
window.location.href = "http://localhost:8000/auth/github/login";

// After OAuth, user lands on callback URL with JSON response
// You need to handle this by setting a redirect URL in the callback
```

### Option 2: Popup-Based Flow (Better UX)

```javascript
// Frontend: Open popup for login
function loginWithGitHub() {
  const popup = window.open(
    "http://localhost:8000/auth/github/login",
    "GitHub Login",
    "width=600,height=700"
  );
  
  // Listen for message from popup
  window.addEventListener("message", (event) => {
    if (event.origin === "http://localhost:8000") {
      const { user, github_account } = event.data;
      console.log("Logged in as:", user.github_login);
      // Save user info to your frontend state
      popup.close();
    }
  });
}
```

### Option 3: Modified Callback with Frontend Redirect (Recommended)

The backend callback should redirect to your frontend with user info. Let me add this feature.

---

## API Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/github/login` | GET | Redirects to GitHub OAuth |
| `/auth/github/callback` | GET | Handles OAuth callback, saves token |
| `/auth/github/status` | GET | Check if OAuth is configured |

---

## Security Notes

1. **Access tokens are encrypted** in the database
2. **Client secret is never exposed** to the frontend
3. **Tokens have scopes** - only `repo` and `user` access granted
4. **HTTPS in production** - always use HTTPS for OAuth in production

