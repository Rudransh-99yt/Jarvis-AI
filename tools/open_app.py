import subprocess
import re
from tools.app_matcher import match

def run(text):
    text = text.lower()
    text = re.sub(r"\b(open|app|apps|jarvis|the|please)\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    app = match(text)

    if not app:
        return "App not found."

    subprocess.run(["open", "-a", app])

    return f"Opened {app}."
