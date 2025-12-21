from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user model with common fields."""

    username: str
    email: EmailStr

    # Global configuration for DB compatibility and clean strings
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class UserCreate(UserBase):
    """Payload for creating a new user account."""

    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "username": "pepito123",
                    "email": "pepito@example.com",
                    "password": "mypass",
                }
            ]
        }
    )


class UserLogin(BaseModel):
    """Payload for authenticating a user."""

    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "pepito@example.com",
                "password": "mypass",
            }
        }
    )


class UserResponse(UserBase):
    """Non-sensitive user information returned by the API."""

    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "username": "pepito123",
                "email": "pepito@example.com",
                "created_at": "2024-01-10T14:30:00",
            }
        },
    )


class UserInDB(UserBase):
    """Internal model that includes the password hash."""

    id: int
    password_hash: str
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "username": "pepito123",
                "email": "pepito@example.com",
                "password_hash": "hashed_password_here",
                "created_at": "2024-01-10T14:30:00",
            }
        },
    )


class Token(BaseModel):
    """JWT token returned after login."""

    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"access_token": "fake_token", "token_type": "bearer"}
        }
    )


class TokenData(BaseModel):
    """Decoded token payload information."""

    sub: Optional[int] = None

    model_config = ConfigDict(json_schema_extra={"example": {"sub": 1}})
