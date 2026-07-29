import sounddevice as sd
import numpy as np
import torch
from scipy.io.wavfile import write
from silero_vad import load_silero_vad, get_speech_timestamps

SAMPLE_RATE = 16000
BLOCK_SIZE = 512

model = load_silero_vad()

def record(filename="voice/input.wav"):
    print("🎤 Listening... (Press Ctrl+C when finished speaking)")

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        blocksize=BLOCK_SIZE,
        dtype="float32",
    )

    stream.start()

    buffer = []

    try:
        while True:
            data, _ = stream.read(BLOCK_SIZE)
            buffer.append(data.copy())

    except KeyboardInterrupt:
        pass

    stream.stop()
    stream.close()

    audio = np.concatenate(buffer, axis=0)

    speech = get_speech_timestamps(
        torch.from_numpy(audio.flatten()),
        model,
        sampling_rate=SAMPLE_RATE,
    )

    if not speech:
        print("❌ No speech detected.")
        return False

    start = speech[0]["start"]
    end = speech[-1]["end"]

    audio = audio[start:end]

    audio16 = (audio * 32767).astype(np.int16)

    write(filename, SAMPLE_RATE, audio16)

    print(f"✅ Saved speech to {filename}")

    return True


if __name__ == "__main__":
    record()
