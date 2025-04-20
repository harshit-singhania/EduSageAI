from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base model for user schema."""
    email: EmailStr = Field(..., min_length=5, max_length=50, description="User's email address")
    first_name: str = Field(..., min_length=1, max_length=50, description="User's full name")
    last_name: str = Field(..., min_length=1, max_length=50, description="User's last name")
    created_at: datetime = Field(..., description="User creation timestamp", default_factory=datetime.utcnow())
    
    
class UserCreate(UserBase):
    """Model for creating a new user."""
    password: str = Field(..., min_length=8, max_length=50, description="User's password")
    
class UserLogin(BaseModel):
    """Model for user login."""
    email: EmailStr = Field(..., min_length=5, max_length=50, description="User's email address")
    password: str = Field(..., min_length=8, max_length=50, description="User's password")
    
class UserUpdate(BaseModel):
    """Model for updating user information."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50, description="User's full name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=50, description="User's last name")
    is_active: Optional[bool] = Field(None, description="Is the user active?")
    password: Optional[str] = Field(None, min_length=8, max_length=50, description="User's password")
    
    class Config: 
        from_attributes = True
    
    
class User(UserBase):
    """schema for user response"""
    id: str 
    is_active: bool = Field(..., description="Is the user active?")
    is_superuser: bool = Field(..., description="Is the user a superuser?")
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: datetime = Field(..., description="User update timestamp")
    
    class Config:
        orm_mode = True  # Enable ORM mode for SQLAlchemy compatibility