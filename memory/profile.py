import json
from pathlib import Path

FILE = Path("memory/profile.json")

ALIASES = {
    "favorite color": "favorite_color",
    "favourite color": "favorite_color",
    "favorite food": "favorite_food",
    "exam date": "exam_date",
    "passport expiration": "passport_expiration",
    "passport expiry": "passport_expiration",
    "location": "city",
}

def normalize(key):
    key = key.strip().lower()
    return ALIASES.get(key, key.replace(" ", "_"))

def load():
    if FILE.exists():
        return json.loads(FILE.read_text())
    return {}

def save(data):
    FILE.parent.mkdir(exist_ok=True)
    FILE.write_text(json.dumps(data, indent=2))

def remember(key, value):
    data = load()
    data[normalize(key)] = value.strip()
    save(data)

def forget(key):
    data = load()
    data.pop(normalize(key), None)
    save(data)

def recall(key):
    return load().get(normalize(key))

def all_memory():
    return load()
