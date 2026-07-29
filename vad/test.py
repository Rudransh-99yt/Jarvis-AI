import torch
from silero_vad import load_silero_vad, read_audio, get_speech_timestamps

model = load_silero_vad()

audio = read_audio("voice/input.wav", sampling_rate=16000)

speech = get_speech_timestamps(audio, model)

print(speech)
