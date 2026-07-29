import subprocess
import re

def run(text):
    m = re.search(r'(\d+)', text)

    if not m:
        return "Say a brightness percentage."

    level = max(0, min(100, int(m.group(1))))
    subprocess.run([
        "brightness",
        str(level/100)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return f"Brightness set to {level}%."
