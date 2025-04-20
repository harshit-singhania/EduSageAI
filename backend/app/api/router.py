import sys 
import os

from fastapi import APIRouter
from .endpoints import chat, auth

api_router = APIRouter()
api_router.include_router(chat.router)
api_router.include_router(auth.router)