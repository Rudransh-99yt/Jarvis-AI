from pathlib import Path
import subprocess

HOME = Path.home()

SEARCH_DIRS = [
    HOME/"Desktop",
    HOME/"Downloads",
    HOME/"Documents"
]

def run(text):
    q = text.lower()

    words = [
        w for w in q.split()
        if w not in {
            "find","search","locate","file","files",
            "named","called","for","jarvis","please"
        }
    ]

    if not words:
        return "What file?"

    key = " ".join(words)

    for folder in SEARCH_DIRS:
        for f in folder.rglob("*"):
            if key in f.name.lower():
                subprocess.run(["open","-R",str(f)])
                return str(f)

    return "File not found."
