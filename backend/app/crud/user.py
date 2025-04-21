from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder

import logging
from typing import List, Optional
import sys
import os

# Add parent directory to sys.path if running directly
if __name__ == "__main__":
	sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Using absolute imports to avoid relative import errors
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password, verify_password
from app.database.session import get_db
from app.core.security import get_user_id_from_token

logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/vi/auth/token")

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate) -> User:
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
    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password,
        is_active=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try: 
        user_id = get_user_id_from_token(token)
        user = get_user_by_id(db, user_id)

        if not user:
            logger.warning(f"User not found for token: {token}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:  
            logger.warning(f"Inactive user: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
def get_current_active_superuser(current_user: User = Depends(get_current_user)) -> User:
    """Get current active superuser."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user doesn't have enough privileges",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
       

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user."""
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def update(db: Session, user_id: str, user_update: UserUpdate) -> User:
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

def delete_user(db: Session, user_id: str) -> User:
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