import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from voice.speak import speak

def run(text):
    speak(text)

if __name__ == "__main__":
    run("Hello Rudransh. I am ready.")
