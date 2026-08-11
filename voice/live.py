import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import audio.state as state

from audio.stream import AudioStream
from audio.buffer import RollingBuffer
from audio.detector import SpeechDetector
from audio.recorder import Recorder


def record():
    mic = AudioStream()
    buffer = RollingBuffer()
    recorder = Recorder()
    detector = SpeechDetector()

    mic.start()

    print("🎤 Listening...")

    # Reset state for every question
    state.RECORDING = False
    state.SILENCE_BLOCKS = 0

    try:
        while True:
            chunk = mic.read()
            buffer.add(chunk)

            # Don't run VAD until we have enough context
            if len(buffer) < 8:
                continue

            speaking = detector.detect(buffer.get())

            if speaking:
                if not state.RECORDING:
                    recorder.clear()
                    recorder.add_many(buffer.get())
                    state.RECORDING = True
                    state.SILENCE_BLOCKS = 0

                recorder.add(chunk)

            elif state.RECORDING:
                recorder.add(chunk)
                state.SILENCE_BLOCKS += 1

                if state.SILENCE_BLOCKS >= 11:
                    recorder.save()
                    recorder.clear()
                    state.RECORDING = False
                    state.SILENCE_BLOCKS = 0
                    break

    finally:
        mic.stop()


if __name__ == "__main__":
    record()
