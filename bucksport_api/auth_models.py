"""Authentication models for user management."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User model for authentication."""
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    role: str  # 'admin', 'board_member', 'fundraising_coordinator', or 'viewer'
    google_id: Optional[str] = Field(default=None, unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    is_active: bool = Field(default=True)


class UserCreate(SQLModel):
    """Schema for creating a new user."""
    email: str
    first_name: str
    last_name: str
    role: str


class UserResponse(SQLModel):
    """Schema for user response."""
    id: int
    email: str
    first_name: str
    last_name: str
    role: str
    created_at: datetime
    last_login: Optional[datetime]


class TokenData(SQLModel):
    """Schema for JWT token data."""
    email: str
    role: str
    exp: int
