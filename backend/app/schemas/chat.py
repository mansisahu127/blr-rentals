from pydantic import BaseModel
from typing import Optional, List

class ChatMessage(BaseModel):
    role: str   # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    reply: str
    listings: List[dict] = []
    session_id: str