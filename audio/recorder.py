import numpy as np
from scipy.io.wavfile import write

from audio.config import SAMPLE_RATE

class Recorder:
    def __init__(self):
        self.frames = []

    def clear(self):
        self.frames = []

    def add(self, chunk):
        self.frames.append(chunk.copy())

    def add_many(self, chunks):
        for chunk in chunks:
            self.frames.append(chunk.copy())

    def save(self, filename="voice/input.wav"):
        if not self.frames:
            return

        audio = np.concatenate(self.frames, axis=0)
        audio = (audio * 32767).astype(np.int16)

        write(filename, SAMPLE_RATE, audio)

        print(f"✅ Saved {filename}")
