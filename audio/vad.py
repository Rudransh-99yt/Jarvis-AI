import webrtcvad
import audio.state as state

vad = webrtcvad.Vad(3)

def process(data):
    if vad.is_speech(data, 16000):
        state.SPEECH_COUNT += 1
        state.SILENCE_COUNT = 0

        if not state.SPEAKING and state.SPEECH_COUNT >= 5:
            state.SPEAKING = True
            print("🗣️ Speech Start")

    else:
        state.SILENCE_COUNT += 1
        state.SPEECH_COUNT = 0

        if state.SPEAKING and state.SILENCE_COUNT >= 20:
            state.SPEAKING = False
            print("🤫 Speech End")
