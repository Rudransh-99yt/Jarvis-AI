import requests
from config.settings import settings

def ask_ai(prompt: str) -> str:
    response = requests.post(
        f"{settings.OLLAMA_URL}/api/generate",
        json={
            "model": settings.MODEL,
            "prompt": prompt,
            "think": False,
            "stream": False
        }
    )

    return response.json()["response"]
