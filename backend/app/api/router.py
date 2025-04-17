import sys 
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import APIRouter
from .endpoints import chat 

api_router = APIRouter()
api_router.include_router(chat.router)