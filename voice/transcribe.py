from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe(filename="voice/input.wav"):
    segments, info = model.transcribe(filename)

    text = " ".join(segment.text for segment in segments)

    print("\nLanguage:", info.language)
    return text.strip()

if __name__ == "__main__":
    print(transcribe())
