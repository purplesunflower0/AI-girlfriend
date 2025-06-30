# main.py

from fastapi import FastAPI, Request
import logging
from pydantic import BaseModel
from models import ChatRequest, ChatResponse
from chat_logic import generate_response
from fastapi.middleware.cors import CORSMiddleware

class ChatRequest(BaseModel):
    user_id: str
    message: str
    personality: str
    
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    print(f"🟡 Received chat request: {req.dict()}")
    try:
        reply = await generate_response(req.user_id, req.message, req.personality)
        print(f"🟢 Final reply to frontend: {reply}")  # 👈 ADD THIS
        return {"reply": reply}
    except Exception as e:
        print(f"🔴 Error inside /chat: {str(e)}")  # 👈 ADD THIS
        return {"reply": "Sorry love, I'm a bit lost right now. Try again?"}

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from memory_store import set_user_personality, get_user_personality

@app.post("/set_personality")
async def set_personality(data: dict):
    user_id = data.get("user_id")
    mood = data.get("mood", "romantic")
    set_user_personality(user_id, mood)
    print(f"🎯 Personality input received: {mood}")
    return {"message": "Personality updated"}


@app.get("/get_personality/{user_id}")
def get_personality(user_id: str):
    mood = get_user_personality(user_id)
    return {"mood": mood}

