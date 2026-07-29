import requests

from config.settings import settings
from brain.system_prompt import SYSTEM_PROMPT
from memory.chat_history import add, get
from memory.remember import process
from memory.profile import all_memory

def ask_ai(prompt: str) -> str:
    process(prompt)

    memory = all_memory()

    memory_text = "\n".join(
        f"- {k}: {v}" for k, v in memory.items()
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT +
            "\n\nKnown facts about the user:\n" +
            memory_text
        }
    ]

    messages.extend(get())
    messages.append({"role": "user", "content": prompt})

    response = requests.post(
        f"{settings.OLLAMA_URL}/api/chat",
        json={
            "model": settings.MODEL,
            "messages": messages,
            "stream": False,
            "think": False
        },
        timeout=120
    )

    response.raise_for_status()

    reply = response.json()["message"]["content"].strip()

    add("user", prompt)
    add("assistant", reply)

    return reply
