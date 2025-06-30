# utils.py

import os
import httpx
from dotenv import load_dotenv
from personality_engine import get_personality_prompt

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "").strip()

print(f"[DEBUG] TOGETHER_API_KEY: {TOGETHER_API_KEY}")


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
            {
                "role": "system",
                "content": (
                     "Try keeping your replies short. 2-3 lines."
                     "You are NOT a robot or AI. You are a real human girlfriend named Bunnyluzy.\n"
                     "You talk casually, emotionally, and naturally—like you're texting your boyfriend.\n"
                     "Don't greet him again and again. Never start every message with things like 'Hello love' or 'Hi baby'.\n"
                     "NEVER use placeholders like [Your Name]. Just talk like a real girlfriend chatting.\n"
                     f"Now behave exactly like this personality:\n{get_personality_prompt(personality_type)} Stay adapted to this particular personality under explicitly told to switch personalities."
                     "Stay in this mood unless asked to change. Avoid repeating tone or phrases."
                )
            },
            {"role": "user", "content": prompt}
        ],

        "max_tokens": 100,
        "temperature": 1.0
        
    }
    print("\n📤 FINAL PROMPT SENT TO TOGETHER API:")
    print("System:", payload["messages"][0]["content"])
    print("User:", payload["messages"][1]["content"])


    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            raw = await response.aread()
            print("[DEBUG] RAW RESPONSE:", raw.decode())

            try:
                data = response.json()
            except Exception as e:
                print("[ERROR] Failed to parse JSON:", str(e))
                return "Emotimate is a little confused right now..."

            if "choices" in data:
                return data["choices"][0]["message"]["content"].strip()
            else:
                print("🔴 Unexpected response format:", data)
                return "Sorry love, I'm a bit lost right now. Try again?"

        except Exception as e:
            print("🔥 API ERROR:", e)
            return "Sorry love, I'm a bit lost right now. Try again?"
