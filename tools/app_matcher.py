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
}

def match(name):
    name = name.lower().strip()

    if name in ALIASES:
        name = ALIASES[name]

    if name in APPS:
        return APPS[name]

    m = get_close_matches(name, APPS.keys(), n=1, cutoff=0.45)

    if m:
        return APPS[m[0]]

    return None
