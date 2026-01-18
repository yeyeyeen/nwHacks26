"""
Pydantic models for User and GitHub Account.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user model."""
    email: Optional[str] = None


class UserCreate(UserBase):
    """Model for creating a new user."""
    pass


class User(UserBase):
    """User model with all fields."""
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class GitHubAccountBase(BaseModel):
    """Base GitHub account model."""
    github_id: int
    github_login: str
    scope: str


class GitHubAccountCreate(GitHubAccountBase):
    """Model for creating a GitHub account."""
    user_id: str
    access_token: str  # Will be encrypted before storage


class GitHubAccount(GitHubAccountBase):
    """GitHub account model with all fields."""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GitHubTokenResponse(BaseModel):
    """Response model for GitHub OAuth token exchange."""
    access_token: str
    scope: str
    token_type: str


class GitHubUser(BaseModel):
    """Model for GitHub user profile."""
    id: int
    login: str
    email: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None


class AuthResponse(BaseModel):
    """Response model for successful authentication."""
    success: bool
    message: str
    user: Optional[dict] = None
    github_account: Optional[dict] = None

