from voice.listen import record
from voice.transcribe import transcribe
from brain.chat import ask_ai
from voice.speak import speak

while True:
    input("\nPress ENTER to talk...")

    record()

    text = transcribe()

    print(f"\nYou: {text}")

    if text.lower() in ["exit", "quit", "goodbye"]:
        break

    reply = ask_ai(text)

    print(f"\nJarvis: {reply}")

    speak(reply)
