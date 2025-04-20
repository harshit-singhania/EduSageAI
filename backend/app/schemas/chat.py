from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    """Request model for chat completions."""
    messages: List[Dict[str, str]]
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 500
    
class ChatResponse(BaseModel):
    """Response model for chat completions."""
    content: str
    