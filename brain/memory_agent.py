import requests

from config.settings import settings

PROMPT = """
You extract long-term memories.

Return ONLY valid JSON.

Format:

{
  "remember": [
    {
      "key": "...",
      "value": "..."
    }
  ]
}

Only remember information useful in future conversations:
- name
- birthday
- preferences
- favorites
- location
- occupation
- goals
- important dates
- reminders
- recurring facts

If nothing should be remembered:

{
  "remember": []
}
"""

def extract(text):
    response = requests.post(
        f"{settings.OLLAMA_URL}/api/chat",
        json={
            "model": settings.MODEL,
            "messages":[
                {"role":"system","content":PROMPT},
                {"role":"user","content":text}
            ],
            "stream":False,
            "think":False
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["message"]["content"]
