# memory_store.py
memory_db = {} 
personality_store = {} # In-memory for now

def load_memory(user_id: str):
    return memory_db.get(user_id, {}).get("chat_history", [])

def update_memory(user_id: str, user_input: str, bot_reply: str):
    if user_id not in memory_db:
        memory_db[user_id] = {"chat_history": []}
    memory_db[user_id]["chat_history"].append({"user": user_input, "bot": bot_reply})

def set_user_personality(user_id: str, mood: str):
    personality_store[user_id] = mood

def get_user_personality(user_id: str) -> str:
    return personality_store.get(user_id, "romantic")