from difflib import get_close_matches
from tools.app_index import installed_apps

APPS = installed_apps()

ALIASES = {
    "chrome": "google chrome",
    "google": "google chrome",
    "calc": "calculator",
    "calculator": "calculator",
    "calendar": "calendar",
    "terminal": "terminal",
    "finder": "finder",
    "notes": "notes",
    "music": "music",
    "spotify": "spotify",
    "code": "visual studio code",
    "vs code": "visual studio code",
    "vscode": "visual studio code",

    # Messaging / communication
    "whatsapp": "whatsapp",
    "whatsapp desktop": "whatsapp",
    "discord": "discord",

    # Development
    "antigravity": "antigravity",
    "anti gravity": "antigravity",
    "anti-gravity": "antigravity",
}

def match(name):
    name = name.lower().strip()

    if name in ALIASES:
        name = ALIASES[name]

    # Exact installed-app match
    if name in APPS:
        return APPS[name]

    # Case-insensitive normalized match
    normalized = {
        app.lower().strip(): app
        for app in APPS
    }

    if name in normalized:
        return normalized[name]

    # Fuzzy match only after exact matching fails
    matches = get_close_matches(
        name,
        normalized.keys(),
        n=1,
        cutoff=0.70,
    )

    if matches:
        return normalized[matches[0]]

    return None
