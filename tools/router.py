import re

from tools.open_app import run as open_app


APP_NAMES = [
    "whatsapp",
    "discord",
    "antigravity",
    "anti gravity",
    "anti-gravity",
    "chrome",
    "google chrome",
    "safari",
    "finder",
    "terminal",
    "calculator",
    "calendar",
    "notes",
    "spotify",
    "music",
    "visual studio code",
    "vs code",
    "vscode",
]


def needs_tools(text):
    text = text.lower()

    patterns = [
        r"\bopen\b",
        r"\bclose\b",
        r"\bquit\b",
        r"\bsearch\b",
        r"\bgoogle\b",
        r"\btime\b",
        r"\bdate\b",
        r"\btimer\b",
        r"\bvolume\b",
        r"\bbrightness\b",
        r"\bcalculator\b",
        r"\bcalculate\b",
        r"\bscreenshot\b",
        r"\bremember\b",
        r"\bshutdown\b",
        r"\brestart\b",
        r"\bsleep\b",
        r"\block\b",
    ]

    return any(re.search(p, text) for p in patterns)


def fast_open_apps(text):
    """
    Handle simple 'open X' commands without planner/LLM.
    Returns None when this is not a simple app-opening request.
    """

    text = text.lower().strip()

    if not re.search(r"\bopen\b", text):
        return None

    # Don't steal complicated requests such as:
    # "open Safari and search for AI news"
    complicated = [
        "search",
        "calculate",
        "remember",
        "brightness",
        "volume",
        "timer",
        "screenshot",
    ]

    if any(word in text for word in complicated):
        return None

    found = []

    for app in APP_NAMES:
        pattern = r"\b" + re.escape(app) + r"\b"

        if re.search(pattern, text):
            if app not in found:
                found.append(app)

    if not found:
        return None

    results = []

    for app in found:
        results.append(open_app(app))

    return results
