from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime
  
class UserCreate(BaseModel):
    """Request model for user registration"""
    username: str
    email: EmailStr
    password: str
  
class UserLogin(BaseModel):
    """Request model for user login"""
    email: EmailStr
    password: str
  
class UserResponse(BaseModel):
    """Response model for user data (no password)"""
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    created_at: Optional[datetime] = None
    
class Token(BaseModel):
    """Response model for JWT Token"""
    access_token: str
    token_type: str = "bearer"
    
class TokenData(BaseModel):
    """Data extracted from JWT Token"""
    user_id: Optional[int] = None
    email: Optional[str] = None