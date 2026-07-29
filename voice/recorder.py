import numpy as np
from scipy.io.wavfile import write

SAMPLE_RATE = 16000

class Recorder:
    def __init__(self):
        self.frames = []

    def clear(self):
        self.frames = []

    def add(self, chunk):
        self.frames.append(chunk.copy())

    def save(self, filename="voice/input.wav"):
        if not self.frames:
            return False

        audio = np.concatenate(self.frames, axis=0)
        audio = (audio * 32767).astype(np.int16)

        write(filename, SAMPLE_RATE, audio)

        print(f"✅ Saved {filename}")

        return True
