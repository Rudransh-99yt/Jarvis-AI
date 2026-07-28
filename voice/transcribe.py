from faster_whisper import WhisperModel

model = WhisperModel(
    "large-v3-turbo",
    device="auto",
    compute_type="int8"
)

def transcribe(audio_file):
    segments, _ = model.transcribe(audio_file)
    return " ".join(segment.text for segment in segments).strip()
