from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import List, Dict, Any, Optional

from app.config import settings
from app.services.llm_service import LLMService
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()
llm_service = LLMService()

@router.post("/chat/completions", response_model=ChatResponse) 
def chat_completions(
    request: ChatRequest
) -> JSONResponse:
    """Get chat completions from the language model."""
    try:
       model_to_use = request.model if request.model else settings.OPENROUTER_MODEL_NAME
       
       response = llm_service.get_completions(
            messages=request.messages,
            model=model_to_use,
            temperature=request.temperature if request.temperature else 0.7,
            max_tokens=request.max_tokens if request.max_tokens else 500
        )
       
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