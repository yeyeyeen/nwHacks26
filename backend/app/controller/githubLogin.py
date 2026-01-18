"""
GitHub OAuth Authentication Controller.

Handles GitHub OAuth flow including:
- Login redirect to GitHub
- Callback handling with token exchange
- User creation/update in Supabase
"""
import os
import json
from urllib.parse import urlencode
import httpx
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv
from app.utils.logger import logger
from app.services.supabase_db import upsert_github_account, get_decrypted_access_token, get_github_account_by_github_id
from app.models.user import AuthResponse

load_dotenv()

router = APIRouter(prefix="/auth/github", tags=["GitHub Auth"])

# GitHub OAuth configuration
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
GITHUB_REDIRECT_URI = os.getenv('GITHUB_REDIRECT_URI', 'http://localhost:8000/auth/github/callback')

# Frontend URL to redirect after successful login (optional)
FRONTEND_REDIRECT_URL = os.getenv('FRONTEND_REDIRECT_URL', None)

# GitHub OAuth URLs
GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"

# Default OAuth scopes
DEFAULT_SCOPES = "repo,user"


@router.get("/login")
async def github_login():
    """
    Initiate GitHub OAuth flow.

    Redirects the user to GitHub's authorization page where they can
    grant access to their account.

    Returns:
        RedirectResponse: Redirects to GitHub OAuth authorization page
    """
    logger.info("=== GitHub OAuth Login initiated ===")

    if not GITHUB_CLIENT_ID:
        logger.error("✗ GITHUB_CLIENT_ID is not configured")
        raise HTTPException(
            status_code=500,
            detail="GitHub OAuth is not configured. Please set GITHUB_CLIENT_ID."
        )

    # Build GitHub authorization URL
    auth_url = (
        f"{GITHUB_AUTHORIZE_URL}"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&scope={DEFAULT_SCOPES}"
        f"&redirect_uri={GITHUB_REDIRECT_URI}"
    )

    logger.info(f"Redirecting to GitHub OAuth authorization")
    logger.debug(f"  Authorization URL: {GITHUB_AUTHORIZE_URL}")
    logger.debug(f"  Client ID: {GITHUB_CLIENT_ID[:8]}..." if GITHUB_CLIENT_ID else "  Client ID: None")
    logger.debug(f"  Scopes: {DEFAULT_SCOPES}")
    logger.debug(f"  Redirect URI: {GITHUB_REDIRECT_URI}")

    return RedirectResponse(url=auth_url)


@router.get("/callback", response_model=AuthResponse)
async def github_callback(code: str = Query(..., description="Authorization code from GitHub")):
    """
    Handle GitHub OAuth callback.

    Exchanges the authorization code for an access token, fetches the user's
    GitHub profile, and creates/updates the user in the database.

    Args:
        code: The authorization code provided by GitHub

    Returns:
        AuthResponse: Authentication result with user information
    """
    logger.info("=== GitHub OAuth Callback received ===")
    logger.debug(f"  Authorization code: {code[:10]}..." if len(code) > 10 else f"  Code: {code}")

    if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
        logger.error("✗ GitHub OAuth credentials are not configured")
        raise HTTPException(
            status_code=500,
            detail="GitHub OAuth is not configured. Please set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET."
        )

    try:
        # Step 1: Exchange code for access token
        logger.info("Step 1: Exchanging authorization code for access token...")
        token_data = await exchange_code_for_token(code)
        access_token = token_data.get('access_token')
        scope = token_data.get('scope', '')

        if not access_token:
            error = token_data.get('error_description', 'Failed to get access token')
            logger.error(f"✗ GitHub token exchange failed: {error}")
            raise HTTPException(status_code=400, detail=error)

        logger.info("✓ Successfully exchanged code for access token")
        logger.debug(f"  Token type: {token_data.get('token_type')}")
        logger.debug(f"  Scope: {scope}")

        # Step 2: Fetch GitHub user profile
        logger.info("Step 2: Fetching GitHub user profile...")
        github_user = await fetch_github_user(access_token)
        github_id = github_user.get('id')
        github_login = github_user.get('login')
        email = github_user.get('email')

        if not github_id or not github_login:
            logger.error("✗ Failed to get GitHub user profile - missing id or login")
            raise HTTPException(status_code=400, detail="Failed to get GitHub user profile")

        logger.info(f"✓ Fetched GitHub profile for user: {github_login}")
        logger.debug(f"  GitHub ID: {github_id}")
        logger.debug(f"  Email: {email}")
        logger.debug(f"  Name: {github_user.get('name')}")

        # Step 3: Create or update user in database
        logger.info("Step 3: Creating/updating user in database...")
        github_account = upsert_github_account(
            github_id=github_id,
            github_login=github_login,
            access_token=access_token,
            scope=scope,
            email=email
        )

        logger.info(f"✓ User authenticated successfully: {github_login}")
        logger.info("=== GitHub OAuth flow completed successfully ===")

        # Prepare the response data
        response_data = {
            "success": True,
            "message": "Successfully authenticated with GitHub",
            "user": {
                "github_id": github_id,
                "github_login": github_login,
                "email": email,
                "name": github_user.get('name'),
                "avatar_url": github_user.get('avatar_url')
            },
            "github_account": {
                "id": github_account.get('id'),
                "user_id": github_account.get('user_id'),
                "github_login": github_login,
                "scope": scope
            }
        }

        # If frontend redirect URL is configured, redirect with user info
        if FRONTEND_REDIRECT_URL:
            # Encode user info as URL parameters for frontend
            params = {
                "success": "true",
                "github_id": str(github_id),
                "github_login": github_login,
                "user_id": github_account.get('user_id', ''),
                "email": email or '',
                "name": github_user.get('name') or '',
                "avatar_url": github_user.get('avatar_url') or ''
            }
            redirect_url = f"{FRONTEND_REDIRECT_URL}?{urlencode(params)}"
            logger.info(f"Redirecting to frontend: {FRONTEND_REDIRECT_URL}")
            return RedirectResponse(url=redirect_url)

        # Otherwise return JSON response
        return AuthResponse(**response_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ GitHub OAuth callback failed: {e}")
        logger.exception("Full exception details:")
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")


async def exchange_code_for_token(code: str) -> dict:
    """
    Exchange authorization code for access token.

    Args:
        code: The authorization code from GitHub

    Returns:
        dict: Token response containing access_token, scope, and token_type
    """
    logger.debug(f"Exchanging code for token at: {GITHUB_TOKEN_URL}")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            GITHUB_TOKEN_URL,
            json={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code
            },
            headers={
                "Accept": "application/json"
            }
        )

        logger.debug(f"Token exchange response status: {response.status_code}")

        if response.status_code != 200:
            logger.error(f"✗ GitHub token exchange failed with status {response.status_code}")
            logger.debug(f"  Response body: {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to exchange code for token"
            )

        result = response.json()
        if 'error' in result:
            logger.error(f"✗ GitHub token exchange error: {result.get('error')}")
            logger.debug(f"  Error description: {result.get('error_description')}")
        else:
            logger.debug("✓ Token exchange successful")

        return result


async def fetch_github_user(access_token: str) -> dict:
    """
    Fetch GitHub user profile using access token.

    Args:
        access_token: The GitHub OAuth access token

    Returns:
        dict: GitHub user profile data
    """
    logger.debug(f"Fetching GitHub user profile from: {GITHUB_USER_URL}")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            GITHUB_USER_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            }
        )

        logger.debug(f"GitHub user API response status: {response.status_code}")

        if response.status_code != 200:
            logger.error(f"✗ GitHub user fetch failed with status {response.status_code}")
            logger.debug(f"  Response body: {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch GitHub user profile"
            )

        user_data = response.json()
        logger.debug(f"✓ Fetched user profile: {user_data.get('login')} (id: {user_data.get('id')})")
        return user_data


@router.get("/status")
async def github_auth_status():
    """
    Check if GitHub OAuth is properly configured.

    Returns:
        dict: Configuration status
    """
    configured = bool(GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET)
    logger.info(f"GitHub OAuth status check - configured: {configured}")
    logger.debug(f"  Client ID set: {bool(GITHUB_CLIENT_ID)}")
    logger.debug(f"  Client Secret set: {bool(GITHUB_CLIENT_SECRET)}")
    logger.debug(f"  Redirect URI: {GITHUB_REDIRECT_URI}")

    return {
        "configured": configured,
        "client_id_set": bool(GITHUB_CLIENT_ID),
        "client_secret_set": bool(GITHUB_CLIENT_SECRET),
        "redirect_uri": GITHUB_REDIRECT_URI
    }


# =============================================================================
# Endpoints that use the saved GitHub token
# =============================================================================

@router.get("/user/{github_id}")
async def get_user_info(github_id: int):
    """
    Get stored GitHub account info for a user.

    Args:
        github_id: The GitHub user ID

    Returns:
        dict: User's GitHub account info (without the token)
    """
    logger.info(f"Fetching stored info for github_id: {github_id}")

    account = get_github_account_by_github_id(github_id)

    if not account:
        logger.warning(f"No account found for github_id: {github_id}")
        raise HTTPException(status_code=404, detail="User not found")

    # Return account info without the encrypted token
    return {
        "id": account.get('id'),
        "user_id": account.get('user_id'),
        "github_id": account.get('github_id'),
        "github_login": account.get('github_login'),
        "scope": account.get('scope'),
        "created_at": account.get('created_at'),
        "updated_at": account.get('updated_at')
    }


@router.get("/user/{github_id}/repos")
async def get_user_repos(github_id: int):
    """
    Fetch repositories for a user using their saved GitHub token.

    Args:
        github_id: The GitHub user ID

    Returns:
        list: User's GitHub repositories
    """
    logger.info(f"Fetching repos for github_id: {github_id}")

    # Get the decrypted token from database
    token = get_decrypted_access_token(github_id)

    if not token:
        logger.error(f"No token found for github_id: {github_id}")
        raise HTTPException(status_code=401, detail="User not authenticated or token not found")

    logger.debug("Using saved token to fetch repositories...")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user/repos",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            },
            params={
                "sort": "updated",
                "per_page": 100
            }
        )

        if response.status_code != 200:
            logger.error(f"Failed to fetch repos: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch repositories")

        repos = response.json()
        logger.info(f"✓ Fetched {len(repos)} repositories for github_id: {github_id}")

        # Return simplified repo info
        return [
            {
                "id": repo.get('id'),
                "name": repo.get('name'),
                "full_name": repo.get('full_name'),
                "description": repo.get('description'),
                "html_url": repo.get('html_url'),
                "clone_url": repo.get('clone_url'),
                "private": repo.get('private'),
                "language": repo.get('language'),
                "stargazers_count": repo.get('stargazers_count'),
                "updated_at": repo.get('updated_at')
            }
            for repo in repos
        ]


@router.get("/user/{github_id}/repo/{repo_name}/commits")
async def get_repo_commits(github_id: int, repo_name: str):
    """
    Fetch recent commits for a repository using the saved GitHub token.

    Args:
        github_id: The GitHub user ID
        repo_name: The repository name (just the repo name, not full path)

    Returns:
        list: Recent commits in the repository
    """
    logger.info(f"Fetching commits for repo '{repo_name}' (github_id: {github_id})")

    # Get the decrypted token and user info
    token = get_decrypted_access_token(github_id)
    account = get_github_account_by_github_id(github_id)

    if not token or not account:
        raise HTTPException(status_code=401, detail="User not authenticated")

    github_login = account.get('github_login')

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{github_login}/{repo_name}/commits",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            },
            params={"per_page": 30}
        )

        if response.status_code != 200:
            logger.error(f"Failed to fetch commits: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch commits")

        commits = response.json()
        logger.info(f"✓ Fetched {len(commits)} commits for {github_login}/{repo_name}")

        return [
            {
                "sha": commit.get('sha'),
                "message": commit.get('commit', {}).get('message'),
                "author": commit.get('commit', {}).get('author', {}).get('name'),
                "date": commit.get('commit', {}).get('author', {}).get('date'),
                "url": commit.get('html_url')
            }
            for commit in commits
        ]
