import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import torch
from silero_vad import load_silero_vad, get_speech_timestamps

import voice.state as state
from voice.mic import start, stop, read
from voice.recorder import Recorder

model = load_silero_vad()
recorder = Recorder()

print("🤖 Live listener ready.")

start()

try:
    while True:
        chunk = read()

        speech = get_speech_timestamps(
            torch.from_numpy(chunk.flatten()),
            model,
            sampling_rate=16000
        )

        if speech:
            if not state.RECORDING:
                print("🎤 Speech detected")
                recorder.clear()
                state.RECORDING = True

            recorder.add(chunk)
            state.SILENCE_BLOCKS = 0

        elif state.RECORDING:
            recorder.add(chunk)
            state.SILENCE_BLOCKS += 1

            if state.SILENCE_BLOCKS > 60:
                recorder.save()
                print("✅ Finished")

                recorder.clear()
                state.RECORDING = False
                state.SILENCE_BLOCKS = 0

except KeyboardInterrupt:
    pass

stop()
