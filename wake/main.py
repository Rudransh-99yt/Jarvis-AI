import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from voice.live import record
from voice.transcribe import transcribe

WAKE_WORDS = (
    "jarvis",
    "hey jarvis",
    "hello jarvis",
)

print("🎤 Waiting for wake word...")

while True:
    record()

    text = transcribe("voice/input.wav").lower().strip()

    if text:
        print("Heard:", text)

    if any(text.startswith(w) for w in WAKE_WORDS):
        print("✅ Wake word detected!")
        break
