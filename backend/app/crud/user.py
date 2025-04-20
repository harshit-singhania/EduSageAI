from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
import sys
import os

# Add parent directory to sys.path if running directly
if __name__ == "__main__":
	sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Using absolute imports to avoid relative import errors
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password, verify_password

def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    """Get user by email."""
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_user_by_id(db: Session, user_id: str) -> Optional[UserModel]:
    """Get user by ID."""
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def create_user(db: Session, user: UserCreate) -> UserModel:
    """Create a new user."""
    # check if user already exists
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    # hash password
    hashed_password = hash_password(user.password)
    db_user = UserModel(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[UserModel]:
    """Authenticate user."""
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return None
    return user

def update(db: Session, user_id: str, user_update: UserUpdate) -> UserModel:
    """Update user."""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
   
    # Update user fields
    
    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
        
    for field, value in update_data.items():
        setattr(db_user, field, value)
        
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str) -> UserModel:
    """Delete user."""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    db.delete(db_user)
    db.commit()
    return db_user