# main.py

from fastapi import FastAPI
from models import ChatRequest, ChatResponse
from chat_logic import generate_response
from fastapi.middleware.cors import CORSMiddleware


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
    reply = await generate_response(req.user_id, req.message, req.personality)
    return ChatResponse(reply=reply)

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from memory_store import set_user_personality, get_user_personality

@app.post("/set_personality")
def set_personality(payload: dict):
    user_id = payload.get("user_id")
    mood = payload.get("mood")
    set_user_personality(user_id, mood)
    return {"message": f"Personality set to {mood} for user {user_id}"}

@app.get("/get_personality/{user_id}")
def get_personality(user_id: str):
    mood = get_user_personality(user_id)
    return {"mood": mood}

