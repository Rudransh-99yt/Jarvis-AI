import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import audio.state as state

from audio.stream import AudioStream
from audio.buffer import RollingBuffer
from audio.detector import SpeechDetector
from audio.recorder import Recorder

mic = AudioStream()
buffer = RollingBuffer()
recorder = Recorder()
detector = SpeechDetector()

mic.start()

print("🤖 Live recorder running...")

try:
    while True:
        chunk = mic.read()
        buffer.add(chunk)

        if len(buffer) < 31:
            continue

        speaking = detector.detect(buffer.get())

        if speaking:
            if not state.RECORDING:
                print("🎤 Recording...")
                recorder.clear()
                state.RECORDING = True
                state.SILENCE_BLOCKS = 0

            recorder.add(chunk)

        elif state.RECORDING:
            recorder.add(chunk)
            state.SILENCE_BLOCKS += 1

            if state.SILENCE_BLOCKS >= 30:
                recorder.save()
                print("✅ Recording saved")

                recorder.clear()
                state.RECORDING = False
                state.SILENCE_BLOCKS = 0

except KeyboardInterrupt:
    pass

mic.stop()
