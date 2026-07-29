import subprocess
import re

def run(text):
    text = text.lower()

    if "mute" in text:
        subprocess.run(["osascript","-e","set volume output muted true"])
        return "Muted."

    if "unmute" in text:
        subprocess.run(["osascript","-e","set volume output muted false"])
        return "Unmuted."

    m = re.search(r'(\d+)', text)

    if m:
        vol = max(0, min(100, int(m.group(1))))
        subprocess.run(["osascript","-e",f"set volume output volume {vol}"])
        return f"Volume set to {vol}%."

    return "Say a volume like 50 percent."
