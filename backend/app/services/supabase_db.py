"""
Supabase database service for user and GitHub account management.
"""
import os
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from supabase import create_client, Client
from app.utils.logger import logger
from app.utils.encryption import encrypt_token, decrypt_token

load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Validate Supabase configuration
if not SUPABASE_URL or not SUPABASE_KEY:
    logger.warning("⚠ SUPABASE_URL or SUPABASE_KEY environment variables are not set!")

# Initialize Supabase client
supabase: Optional[Client] = None


def get_supabase() -> Client:
    """Get Supabase client instance with lazy initialization."""
    global supabase

    if supabase is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            logger.error("✗ Supabase configuration is not set in environment")
            raise ValueError("Supabase configuration is not set in environment")

        logger.debug(f"Connecting to Supabase at: {SUPABASE_URL[:30]}...")
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("✓ Supabase client initialized successfully")

    return supabase


def get_or_create_user(email: Optional[str] = None) -> Dict[str, Any]:
    """
    Get existing user by email or create a new one.

    Args:
        email: Optional email address

    Returns:
        User record dictionary
    """
    logger.debug(f"get_or_create_user called with email: {email}")
    client = get_supabase()

    if email:
        # Try to find existing user by email
        logger.debug(f"Searching for existing user with email: {email}")
        result = client.table('users').select('*').eq('email', email).execute()
        if result.data:
            logger.info(f"✓ Found existing user by email: {result.data[0]['id']}")
            return result.data[0]
        logger.debug(f"No existing user found with email: {email}")

    # Create new user
    logger.debug("Creating new user record...")
    user_data = {
        'email': email,
        'created_at': datetime.now(timezone.utc).isoformat()
    }
    result = client.table('users').insert(user_data).execute()

    if result.data:
        logger.info(f"✓ Created new user: {result.data[0]['id']}")
        return result.data[0]

    logger.error("✗ Failed to create user - no data returned from insert")
    raise Exception("Failed to create user")


def get_github_account_by_github_id(github_id: int) -> Optional[Dict[str, Any]]:
    """
    Get GitHub account by GitHub user ID.

    Args:
        github_id: The GitHub user ID

    Returns:
        GitHub account record or None if not found
    """
    logger.debug(f"Looking up GitHub account for github_id: {github_id}")
    client = get_supabase()
    result = client.table('github_accounts').select('*').eq('github_id', github_id).execute()

    if result.data:
        logger.info(f"✓ Found GitHub account for github_id: {github_id}")
        return result.data[0]

    logger.debug(f"No GitHub account found for github_id: {github_id}")
    return None


def create_github_account(
    user_id: str,
    github_id: int,
    github_login: str,
    access_token: str,
    scope: str
) -> Dict[str, Any]:
    """
    Create a new GitHub account record.

    Args:
        user_id: The user ID (FK to users table)
        github_id: The GitHub user ID
        github_login: The GitHub username
        access_token: The OAuth access token (will be encrypted)
        scope: The OAuth scope granted

    Returns:
        Created GitHub account record
    """
    logger.info(f"Creating GitHub account for user: {github_login} (github_id: {github_id})")
    logger.debug(f"  user_id: {user_id}, scope: {scope}")

    client = get_supabase()

    logger.debug("Encrypting access token...")
    encrypted_token = encrypt_token(access_token)
    logger.debug("✓ Token encrypted successfully")

    now = datetime.now(timezone.utc).isoformat()

    account_data = {
        'user_id': user_id,
        'github_id': github_id,
        'github_login': github_login,
        'access_token': encrypted_token,
        'scope': scope,
        'created_at': now,
        'updated_at': now
    }

    logger.debug("Inserting GitHub account into database...")
    result = client.table('github_accounts').insert(account_data).execute()

    if result.data:
        logger.info(f"✓ Created GitHub account for user: {github_login} (id: {result.data[0].get('id')})")
        return result.data[0]

    logger.error(f"✗ Failed to create GitHub account for user: {github_login}")
    raise Exception("Failed to create GitHub account")


def update_github_account(
    github_id: int,
    access_token: str,
    scope: str,
    github_login: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an existing GitHub account record.

    Args:
        github_id: The GitHub user ID
        access_token: The new OAuth access token (will be encrypted)
        scope: The new OAuth scope granted
        github_login: Optional updated GitHub username

    Returns:
        Updated GitHub account record
    """
    logger.info(f"Updating GitHub account for github_id: {github_id}")
    logger.debug(f"  github_login: {github_login}, scope: {scope}")

    client = get_supabase()

    logger.debug("Encrypting new access token...")
    encrypted_token = encrypt_token(access_token)
    logger.debug("✓ Token encrypted successfully")

    update_data = {
        'access_token': encrypted_token,
        'scope': scope,
        'updated_at': datetime.now(timezone.utc).isoformat()
    }

    if github_login:
        update_data['github_login'] = github_login

    logger.debug(f"Updating GitHub account in database...")
    result = client.table('github_accounts').update(update_data).eq('github_id', github_id).execute()

    if result.data:
        logger.info(f"✓ Updated GitHub account for github_id: {github_id}")
        return result.data[0]

    logger.error(f"✗ Failed to update GitHub account for github_id: {github_id}")
    raise Exception("Failed to update GitHub account")


def upsert_github_account(
    github_id: int,
    github_login: str,
    access_token: str,
    scope: str,
    email: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create or update a GitHub account. Creates user if needed.

    Args:
        github_id: The GitHub user ID
        github_login: The GitHub username
        access_token: The OAuth access token
        scope: The OAuth scope granted
        email: Optional email from GitHub profile

    Returns:
        The GitHub account record (created or updated)
    """
    logger.info(f"=== Upserting GitHub account for: {github_login} (github_id: {github_id}) ===")
    logger.debug(f"  email: {email}, scope: {scope}")

    # Check if GitHub account exists
    logger.debug("Checking for existing GitHub account...")
    existing_account = get_github_account_by_github_id(github_id)

    if existing_account:
        # Update existing account
        logger.info(f"Found existing account, updating...")
        return update_github_account(
            github_id=github_id,
            access_token=access_token,
            scope=scope,
            github_login=github_login
        )
    else:
        # Create new user and GitHub account
        logger.info(f"No existing account found, creating new user and GitHub account...")
        user = get_or_create_user(email=email)
        return create_github_account(
            user_id=user['id'],
            github_id=github_id,
            github_login=github_login,
            access_token=access_token,
            scope=scope
        )


def get_decrypted_access_token(github_id: int) -> Optional[str]:
    """
    Get the decrypted access token for a GitHub account.

    Args:
        github_id: The GitHub user ID

    Returns:
        The decrypted access token or None if not found
    """
    logger.debug(f"Retrieving access token for github_id: {github_id}")
    account = get_github_account_by_github_id(github_id)

    if account and account.get('access_token'):
        logger.debug(f"Decrypting access token for github_id: {github_id}")
        token = decrypt_token(account['access_token'])
        logger.info(f"✓ Retrieved and decrypted access token for github_id: {github_id}")
        return token

    logger.warning(f"No access token found for github_id: {github_id}")
    return None

