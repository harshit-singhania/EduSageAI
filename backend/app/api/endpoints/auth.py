from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Dict, Any

from app import crud
from app.schemas.user import UserCreate, User
from app.core.security import create_access_token, create_refresh_token, create_tokens, get_user_id_from_token
from app.database.session import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register", response_model=User) 
def register(user_data: UserCreate, db: Session = Depends(get_db)) -> Any:
    user = crud.user.create_user(db=db, user=user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), 
          db: Session = Depends(get_db)) -> Any: 
    user = crud.user.authenticate_user(db=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    tokens = create_tokens(data={"sub": user.id})
    return tokens