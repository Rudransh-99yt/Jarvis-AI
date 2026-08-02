from pathlib import Path
from datetime import datetime
import re

NOTES = Path.home() / "Desktop" / "Jarvis_Notes"
NOTES.mkdir(exist_ok=True)

def run(text):
    t = text.lower()

    if "remember" in t or "note" in t or "save" in t:
        s = re.sub(r".*(remember|note|save)\s*", "", text, flags=re.I).strip()
        if not s:
            return "Nothing to save."

        f = NOTES / f"{datetime.now():%Y-%m-%d}.txt"

        with open(f, "a") as fp:
            fp.write(s + "\n")

        return "Note saved."

    if "show" in t or "read" in t:
        files = sorted(NOTES.glob("*.txt"))
        if not files:
            return "No notes."

        return files[-1].read_text()

    return "Unknown notes command."
