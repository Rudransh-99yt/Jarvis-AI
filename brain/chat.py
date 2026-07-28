import ollama
from config.settings import settings

with open("config/personality.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

def chat(prompt: str) -> str:
    messages.append({"role": "user", "content": prompt})

    response = ollama.chat(
        model=settings.MODEL,
        messages=messages,
    )

    reply = response["message"]["content"]
    messages.append({"role": "assistant", "content": reply})

    return reply
