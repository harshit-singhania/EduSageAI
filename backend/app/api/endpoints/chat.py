from fastapi import APIRouter, Depends, HTTPException
import sys 
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from schemas.chat_schemas import ChatRequest, ChatResponse, ErrorResponse
from services.llm_service import LLMService
from config import settings

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)
llm_service = LLMService()

# GET /chat
# This endpoint is for testing purposes only.
# It returns a simple message indicating that the chat endpoint is working.
@router.get("/")
async def get_chat():
    return {"message": "Chat endpoint"}

# POST /chat/completion
# This endpoint is used to get a chat completion from the language model.
@router.post(
    "/completion",
    response_model=ChatResponse,
)
async def chat_completion(request: ChatRequest): 
    try:
        messages = [message.dict() for message in request.messages]
        
        # get response 
        model_to_use = request.model if request.model else settings.OPENROUTER_MODEL_NAME
        temperature = request.temperature if request.temperature else 0.7
        max_tokens = request.max_tokens if request.max_tokens else 500
        
        completion = llm_service.get_completions(
            messages=messages,
            model=model_to_use,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        if isinstance(completion, dict) and "error" in completion:
            raise HTTPException(status_code=500, detail=completion["error"])
        
        return ChatResponse(
            response=completion,
            tokens_used=len(completion.split()),
            error=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def list_models():
    """List available LLM models"""
    return {
        "models": [
            {"id": "anthropic/claude-3-haiku-20240307", "name": "Claude 3 Haiku"},
            {"id": "anthropic/claude-3-sonnet-20240229", "name": "Claude 3 Sonnet"},
            {"id": "anthropic/claude-3-opus-20240229", "name": "Claude 3 Opus"},
            {"id": "openai/gpt-4-turbo", "name": "GPT-4 Turbo"},
            {"id": "openai/gpt-4-vision", "name": "GPT-4 Vision"},
            {"id": "deepseek/deepseek-r1-zero", "name": "DeepSeek R1 Zero"}
        ]
    }