# models.py

from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    message: str
    personality: str = "romantic"

class ChatResponse(BaseModel):
    reply: str
