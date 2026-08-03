import numpy as np
import torch
import os
import sys

from silero_vad import get_speech_timestamps
from silero_vad.model import OnnxWrapper
from audio.config import SAMPLE_RATE

if getattr(sys, "frozen", False):
    model_path = os.path.join(
        sys._MEIPASS,
        "silero_vad",
        "data",
        "silero_vad.onnx",
    )
else:
    import silero_vad
    model_path = os.path.join(
        os.path.dirname(silero_vad.__file__),
        "data",
        "silero_vad.onnx",
    )

model = OnnxWrapper(model_path, force_onnx_cpu=True)


class SpeechDetector:
    def detect(self, chunks):
        if not chunks:
            return False

        audio = np.concatenate(chunks, axis=0).flatten()

        speech = get_speech_timestamps(
            torch.from_numpy(audio),
            model,
            sampling_rate=SAMPLE_RATE,
        )

        return len(speech) > 0
