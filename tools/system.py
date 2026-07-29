import subprocess

COMMANDS = {
    "sleep": ["pmset", "sleepnow"],
    "lock": ["osascript", "-e", 'tell application "System Events" to keystroke "q" using {control down, command down}'],
}

def run(text):
    text = text.lower()

    if "lock" in text:
        subprocess.run(COMMANDS["lock"])
        return "Locked Mac."

    if "sleep" in text:
        subprocess.run(COMMANDS["sleep"])
        return "Sleeping Mac."

    return "System command not found."
