import sounddevice as sd
from scipy.io.wavfile import write

def record(filename="voice/input.wav", samplerate=16000):
    print("Speak... (Press Ctrl+C to stop)")

    recording = []

    def callback(indata, frames, time, status):
        recording.extend(indata.copy())

    with sd.InputStream(
        samplerate=samplerate,
        channels=1,
        dtype="int16",
        callback=callback,
    ):
        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass

    import numpy as np
    write(filename, samplerate, np.array(recording, dtype="int16"))
    print("Saved:", filename)
