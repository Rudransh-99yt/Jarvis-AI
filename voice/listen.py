import sounddevice as sd
import numpy as np
import webrtcvad
from scipy.io.wavfile import write

def record(filename="voice/input.wav"):
    fs = 16000
    vad = webrtcvad.Vad(2)

    print("🎤 Speak... (auto-stops after silence)")

    frames = []
    silence = 0

    stream = sd.RawInputStream(
        samplerate=fs,
        blocksize=480,
        dtype="int16",
        channels=1
    )

    stream.start()

    try:
        while True:
            data, overflowed = stream.read(480)

            frames.append(np.frombuffer(data, dtype=np.int16))

            if vad.is_speech(data, fs):
                silence = 0
            else:
                silence += 1

            if len(frames) > 20 and silence > 30:
                break

    finally:
        stream.stop()
        stream.close()

    audio = np.concatenate(frames)
    write(filename, fs, audio)

    print("✅ Saved:", filename)

if __name__ == "__main__":
    record()
