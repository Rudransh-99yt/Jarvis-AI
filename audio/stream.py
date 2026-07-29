import sounddevice as sd
from audio.config import SAMPLE_RATE, BLOCK_SIZE

class AudioStream:
    def __init__(self):
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            blocksize=BLOCK_SIZE,
            dtype="float32",
        )

    def start(self):
        self.stream.start()

    def read(self):
        data, _ = self.stream.read(BLOCK_SIZE)
        return data

    def stop(self):
        self.stream.stop()
        self.stream.close()
