import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from brain.chat import ask_ai

def run(text):
    reply = ask_ai(text)

    print(reply)

    return reply

if __name__ == "__main__":
    run("Who are you?")
