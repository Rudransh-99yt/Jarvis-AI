import time
import mlx_whisper

MODEL = "mlx-community/whisper-turbo"


def transcribe(filename="voice/input.wav"):
    start = time.time()

    result = mlx_whisper.transcribe(
        filename,
        path_or_hf_repo=MODEL,
        language="en",
        verbose=False,
        condition_on_previous_text=False,
        temperature=0,
    )

    elapsed = time.time() - start

    text = result["text"].strip()

    print(f"📝 Whisper: {elapsed:.2f}s")
    print(f"🗣️ Text: {text}")

    return text


if __name__ == "__main__":
    print(transcribe())
