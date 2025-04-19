from pydantic import BaseModel 
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel): 
    messages: List[Dict[str, str]]
    model: Optional[str] = "gpt-3.5-turbo"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 500
    
class ChatResponse(BaseModel):
    content: str 
    
    