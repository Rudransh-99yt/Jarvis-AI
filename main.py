from voice.listen import record
from voice.transcribe import transcribe
from brain.chat import ask_ai
from voice.speak import speak

print("🤖 Jarvis is running...")

while True:
    record()

    text = transcribe().strip()

    if not text:
        continue

    print(f"\nYou: {text}")

    if text.lower() in ["exit", "quit", "goodbye"]:
        speak("Goodbye!")
        break

    reply = ask_ai(text)

    print(f"\nJarvis: {reply}")

    speak(reply)
