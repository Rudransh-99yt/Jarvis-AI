
import time

from voice.live import record
from voice.fast_transcribe import transcribe
from voice.fast_speak import speak

from brain.jarvis_brain import think
from brain.tools import execute


def run():
    print()
    print("========================================")
    print("🤖 JARVIS FAST MODE")
    print("========================================")
    print("All AI models stay loaded.")
    print("No separate planner.")
    print("Press Ctrl+C to stop.")
    print()

    question = 0

    while True:
        question += 1

        print()
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📊 Question #{question}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        total_start = time.time()

        # -------------------------
        # RECORD
        # -------------------------

        print("🎤 Listening...")
        record()

        # -------------------------
        # STT
        # -------------------------

        text = transcribe("voice/input.wav")

        if not text:
            print("⚠️ Nothing heard.")
            continue

        # -------------------------
        # BRAIN
        # -------------------------

        plan = think(text)

        print("🧩 Decision:", plan)

        # -------------------------
        # EXECUTE / ANSWER
        # -------------------------

        result = execute(plan)

        print(f"🤖 {result}")

        # -------------------------
        # TTS
        # -------------------------

        speak(result)

        print(
            f"🚀 TOTAL: "
            f"{time.time() - total_start:.2f}s"
        )
