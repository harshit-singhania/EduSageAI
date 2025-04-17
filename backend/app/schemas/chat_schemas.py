from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ChatMessage(BaseModel): 
    """Schema for a chat message."""
    role: str = Field(..., description="Role of the message sender (user, assistant, system)")
    content: str = Field(..., description="Content of the message")
    
class ChatRequest(BaseModel):
    """Schema for a chat request."""
    messages: List[ChatMessage] = Field(..., description="List of chat messages")
    model: Optional[str] = Field(None, description="Model name")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    max_tokens: Optional[int] = Field(500, description="Maximum number of tokens to generate")
    
class ChatResponse(BaseModel):
    """Schema for a chat response."""
    response: str = Field(..., description="Response from the model")
    tokens_used: Optional[int] = Field(None, description="Number of tokens used in the response")
    error: Optional[str] = Field(None, description="Error message if any")
    
class ErrorResponse(BaseModel):
    """Schema for an error response."""
    error: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    
    