"""
Token encryption utilities using Fernet symmetric encryption.
"""
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()

# Get encryption key from environment
TOKEN_ENCRYPTION_KEY = os.getenv('TOKEN_ENCRYPTION_KEY')

# Validate encryption key is set
if not TOKEN_ENCRYPTION_KEY:
    logger.warning("⚠ TOKEN_ENCRYPTION_KEY environment variable is not set!")
    logger.warning("⚠ Generate one using: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\"")

def get_fernet() -> Fernet:
    """Get Fernet instance for encryption/decryption."""
    if not TOKEN_ENCRYPTION_KEY:
        raise ValueError("TOKEN_ENCRYPTION_KEY is not configured in environment")
    return Fernet(TOKEN_ENCRYPTION_KEY.encode())


def encrypt_token(token: str) -> str:
    """
    Encrypt a token using Fernet symmetric encryption.

    Args:
        token: The plaintext token to encrypt

    Returns:
        The encrypted token as a string
    """
    try:
        fernet = get_fernet()
        encrypted = fernet.encrypt(token.encode())
        return encrypted.decode()
    except Exception as e:
        logger.error(f"Failed to encrypt token: {e}")
        raise


def decrypt_token(encrypted_token: str) -> str:
    """
    Decrypt an encrypted token.

    Args:
        encrypted_token: The encrypted token string

    Returns:
        The original plaintext token
    """
    try:
        fernet = get_fernet()
        decrypted = fernet.decrypt(encrypted_token.encode())
        return decrypted.decode()
    except Exception as e:
        logger.error(f"Failed to decrypt token: {e}")
        raise

