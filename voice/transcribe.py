from faster_whisper import WhisperModel

model = WhisperModel(
    "turbo",
    device="cpu",
    compute_type="int8"
)

def transcribe(filename="voice/input.wav"):
    segments, info = model.transcribe(
        filename,
        beam_size=1,
        vad_filter=True
    )

    text = " ".join(segment.text for segment in segments)

    print("\nLanguage:", info.language)
    return text.strip()

if __name__ == "__main__":
    print(transcribe())
