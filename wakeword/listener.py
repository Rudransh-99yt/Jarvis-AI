import tempfile
import sounddevice as sd
import soundfile as sf
import mlx_whisper

RATE = 16000

WAKE_WORDS = [
    "jarvis",
    "hey jarvis",
    "hello jarvis",
]

def detected(text):
    text = text.lower().strip()

    if any(w in text for w in WAKE_WORDS):
        return True

    return any(x in text for x in [
        "jervis",
        "javis",
        "jarvice",
        "jabez",
    ])

print("🎤 Waiting for Jarvis...")

while True:
    audio = sd.rec(int(1.5 * RATE), samplerate=RATE, channels=1, dtype="float32")
    sd.wait()

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(tmp.name, audio, RATE)

    result = mlx_whisper.transcribe(
        tmp.name,
        path_or_hf_repo="mlx-community/whisper-turbo"
    )

    text = result["text"].lower().strip()

    if text:
        print("Heard:", text)

    if detected(text):
        print("✅ Wake word detected!")
        break
