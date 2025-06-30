# chat_logic.py
from memory_store import load_memory, update_memory
from personality_engine import get_personality_prompt

from config import BASE_PROMPT
from utils import call_together_api

async def generate_response(user_id: str, user_input: str, personality: str = "romantic") -> str:
    # Load memory and personality
    history = load_memory(user_id)
    personality_prompt = get_personality_prompt(personality)
    print("🎯 Personality input received:", personality)
    print("📜 Prompt being used:\n", personality_prompt)


    # Build prompt
    full_prompt = BASE_PROMPT.format(
        personality=personality_prompt,
        history="\n".join([f"You: {h['user']} \n{h['bot']}" for h in history]),
        input=user_input
    )

    # Get LLM response
    reply = await call_together_api(full_prompt)

    # Save to memory
    update_memory(user_id, user_input, reply)

    return reply
