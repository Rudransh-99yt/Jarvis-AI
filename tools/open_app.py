import subprocess

ALIASES = {
    "safari": "Safari",
    "spotify": "Spotify",
    "discord": "Discord",

    "vs code": "Visual Studio Code",
    "v s code": "Visual Studio Code",
    "visual studio code": "Visual Studio Code",
    "code": "Visual Studio Code",
    "this code": "Visual Studio Code",

    "photo booth": "Photo Booth",
    "photos": "Photos",
    "terminal": "Terminal",
    "finder": "Finder",
    "notes": "Notes",
    "calendar": "Calendar",
    "chrome": "Google Chrome",
}

def run(text):
    text = text.lower()

    for key, app in ALIASES.items():
        if key in text:
            subprocess.run(["open", "-a", app])
            return f"Opened {app}."

    return "App not found."
