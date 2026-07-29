import subprocess
import re
from tools.app_index import installed_apps

APPS = installed_apps()

ALIASES = {
    "chrome": "google chrome",
    "calc": "calculator",
    "anti gravity": "antigravity",
    "anti-gravity": "antigravity",
    "vs code": "visual studio code",
    "vscode": "visual studio code",
}

def run(text):
    text = text.lower()

    for a, b in ALIASES.items():
        text = text.replace(a, b)

    text = re.sub(r"\b(open|app|apps|jarvis|the|please)\b", " ", text)
    text = re.sub(r"\s+", " ", text)

    opened = []

    for key, app in APPS.items():
        if re.search(rf"\b{re.escape(key)}\b", text):
            try:
                subprocess.run(["open", "-a", app], check=True)
                opened.append(f"Opened {app}")
            except:
                opened.append(f"Couldn't open {app}")

    return "\n".join(opened) if opened else "App not found."
