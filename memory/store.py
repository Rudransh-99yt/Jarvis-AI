import json
from pathlib import Path

FILE = Path("memory/data.json")

if not FILE.exists():
    FILE.write_text("{}")

def load():
    return json.loads(FILE.read_text())

def save(data):
    FILE.write_text(json.dumps(data, indent=2))

def remember(key, value):
    data = load()
    data[key] = value
    save(data)
    return "Remembered."

def recall(key):
    return load().get(key)
