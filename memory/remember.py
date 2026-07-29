import json

from brain.memory_agent import extract
from memory.profile import remember

def process(text):
    try:
        data = json.loads(extract(text))

        for item in data.get("remember", []):
            remember(item["key"], item["value"])

    except Exception:
        pass
