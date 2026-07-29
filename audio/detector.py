import numpy as np
import torch
from silero_vad import load_silero_vad, get_speech_timestamps

from audio.config import SAMPLE_RATE

model = load_silero_vad()

class SpeechDetector:
    def detect(self, chunks):
        if not chunks:
            return False

        audio = np.concatenate(chunks, axis=0).flatten()

        speech = get_speech_timestamps(
            torch.from_numpy(audio),
            model,
            sampling_rate=SAMPLE_RATE
        )

        return len(speech) > 0
