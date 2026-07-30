import time
import sounddevice as sd
from audio.config import SAMPLE_RATE, BLOCK_SIZE

class AudioStream:
    def __init__(self):
        self.stream = None

    def _open(self):
        if self.stream:
            try:
                self.stream.close()
            except:
                pass

        device = sd.default.device[0]
        info = sd.query_devices(device, "input")
        print(f"🎤 Using: {info['name']}")

        self.stream = sd.InputStream(
            device=device,
            samplerate=SAMPLE_RATE,
            channels=1,
            blocksize=BLOCK_SIZE,
            dtype="float32",
        )

    def start(self):
        self._open()
        self.stream.start()

    def read(self):
        while True:
            try:
                data, _ = self.stream.read(BLOCK_SIZE)
                return data
            except Exception:
                print("🔄 Microphone changed. Reconnecting...")
                time.sleep(1)
                self._open()
                self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
