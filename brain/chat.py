import requests
from config.settings import settings

SYSTEM_PROMPT = """
You are Jarvis, a personal AI assistant created by Rudransh.
Never say you were created by Alibaba Cloud or mention Qwen.
Be concise, helpful, and friendly.
"""

def ask_ai(prompt: str) -> str:
    response = requests.post(
        f"{settings.OLLAMA_URL}/api/generate",
        json={
            "model": settings.MODEL,
            "system": SYSTEM_PROMPT,
            "prompt": prompt,
            "think": False,
            "stream": False
        }
    )

    return response.json()["response"]
