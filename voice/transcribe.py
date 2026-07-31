import mlx_whisper

MODEL = "mlx-community/whisper-turbo"

def transcribe(filename="voice/input.wav"):
    result = mlx_whisper.transcribe(
        filename,
        path_or_hf_repo=MODEL,
        language="en",
    )

    print("\nLanguage:", result["language"])
    return result["text"].strip()

if __name__ == "__main__":
    print(transcribe())
