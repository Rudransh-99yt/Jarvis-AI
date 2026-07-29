from voice.listen import record
from voice.transcribe import transcribe
from brain.chat import ask_ai
from voice.speak import speak


def run_once():
    record()

    text = transcribe().strip()

    if not text:
        return

    print(f"\nYou: {text}")

    reply = ask_ai(text)

    print(f"\nJarvis: {reply}")

    speak(reply)
