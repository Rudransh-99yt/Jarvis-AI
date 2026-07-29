import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from voice.transcribe import transcribe

def run():
    text = transcribe("voice/input.wav").strip()

    print(text)

    return text

if __name__ == "__main__":
    run()
