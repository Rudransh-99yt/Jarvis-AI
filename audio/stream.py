import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import sounddevice as sd
import audio.vad as vad

FS = 16000
BLOCK = 480

stream = sd.RawInputStream(
    samplerate=FS,
    blocksize=BLOCK,
    channels=1,
    dtype="int16",
)

stream.start()
print("🎤 Listening...")

try:
    while True:
        data, _ = stream.read(BLOCK)
        vad.process(data)

except KeyboardInterrupt:
    pass

stream.stop()
stream.close()
