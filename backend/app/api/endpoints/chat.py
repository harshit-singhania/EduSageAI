from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import logging
import traceback
from typing import List, Dict, Any, Optional

from app.config import settings
from app.services.llm import LLMService
from app.schemas.chat import ChatRequest, ChatResponse
from app.models.user import User
from app.crud.user import get_current_user

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter()
llm_service = LLMService()

@router.post("/chat/completions", 
             response_model=ChatResponse) 
def chat_completions(
    request: ChatRequest, 
    current_user: User = Depends(get_current_user)
) -> JSONResponse:
    """Get chat completions from the language model."""
    try:
        logger.info(f"Chat request received from user: {current_user.email}")

        model_to_use = request.model if request.model else settings.OPENROUTER_MODEL_NAME
        
        logger.info(f"Using model: {model_to_use}")
        response = llm_service.get_completions(
                messages=request.messages,
                model=model_to_use,
                temperature=request.temperature if request.temperature else 0.7,
                max_tokens=request.max_tokens if request.max_tokens else 500
            )
        
        logger.info(f"Chat response generated successfully")
        logger.debug(f"Chat response: {response}")
        
        return JSONResponse(
                content = {
                    "content": response
                }
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )