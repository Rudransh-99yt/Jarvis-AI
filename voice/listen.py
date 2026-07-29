import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

FS = 16000

def record(filename="voice/input.wav", seconds=5):
    print("🎤 Listening...")

    audio = sd.rec(
        int(seconds * FS),
        samplerate=FS,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    write(filename, FS, audio)

    print(f"✅ Saved: {filename}")

if __name__ == "__main__":
    record()
