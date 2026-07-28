import sounddevice as sd
from scipy.io.wavfile import write

def record(filename="voice/input.wav"):
    print("Opening microphone...")

    fs = 16000
    seconds = 5

    recording = sd.rec(
        int(seconds * fs),
        samplerate=fs,
        channels=1,
        dtype="int16"
    )

    print("Recording...")
    sd.wait()

    write(filename, fs, recording)

    print(f"Saved to {filename}")

if __name__ == "__main__":
    record()
