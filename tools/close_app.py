import subprocess
import re
from tools.app_index import installed_apps

APPS = installed_apps()

ALIASES = {
    "chrome": "google chrome",
    "vs code": "visual studio code",
    "vscode": "visual studio code",
    "anti gravity": "antigravity",
    "anti-gravity": "antigravity",
}

def run(text):
    text = text.lower()

    for a, b in ALIASES.items():
        text = text.replace(a, b)

    text = re.sub(r"\b(close|quit|exit|app|apps|jarvis|the|please)\b", " ", text)
    text = re.sub(r"\s+", " ", text)

    closed = []

    for key, app in APPS.items():
        if re.search(rf"\b{re.escape(key)}\b", text):
            try:
                subprocess.run(
                    ["osascript", "-e", f'tell application "{app}" to quit'],
                    check=True
                )
                closed.append(f"Closed {app}")
            except:
                closed.append(f"Couldn't close {app}")

    return "\n".join(closed) if closed else "App not found."
