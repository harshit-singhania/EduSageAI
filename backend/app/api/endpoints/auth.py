from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from typing import Dict, Any
import logging 
import traceback
import sys

from app import crud
from app.schemas.user import UserCreate, User
from app.core.security import create_access_token, create_refresh_token, create_tokens, get_user_id_from_token
from app.database.session import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try: 
        logger.info(f"Login attempt for user: {form_data.username}")
        user = crud.user.authenticate_user(db=db, email=form_data.username, password=form_data.password)
        if not user:
            logger.warning(f"Invalid credentials for user: {form_data.username}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        logger.info(f"User {form_data.username} authenticated successfully")
        
        logger.info("Creating tokens")
        access_token = create_access_token(data={"sub": user.id})
        logger.info("Access token created")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "status_code": status.HTTP_200_OK,
            "message": "Login successful",
            "user": jsonable_encoder(user),
        }
    except HTTPException as e:
        logger.error(f"Error in login: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Unexpected error in login: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.get("/test", status_code=200) 
def test_auth_route() -> Dict[str, str]: 
    return {"message": "Auth route is working!"}