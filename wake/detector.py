from voice.live import record
from voice.transcribe import transcribe
from wake.config import WAKE_WORDS

def wait_for_wake():
    while True:
        record()
        text = transcribe("voice/input.wav").lower().strip()

        if text:
            print("👂", text)

        if any(w in text for w in WAKE_WORDS):
            print("✅ Wake word detected!")
            return
