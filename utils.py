# utils.py

import os
import httpx
from dotenv import load_dotenv
from personality_engine import get_personality_prompt

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

async def call_together_api(prompt: str, personality_type="romantic") -> str:
    url = "https://api.together.xyz/v1/chat/completions"
    
    

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = get_personality_prompt(personality_type)
    
    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "You are a sweet, flirty AI girlfriend named Emotimate."},
            {"role": "user", "content": prompt}
        ],
        
        "max_tokens": 100,
        "temperature": 0.9
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        data = response.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"].strip()
        else:
            return "Sorry love, I'm a bit lost right now. Try again?"
