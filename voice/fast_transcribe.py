
import time

from brain.runtime import STT


def transcribe(audio_path):
    t = time.time()

    result = STT.generate(audio_path)

    text = getattr(result, "text", str(result)).strip()

    elapsed = time.time() - t

    print(f"📝 Parakeet: {elapsed:.2f}s")
    print(f"👤 {text}")

    return text
