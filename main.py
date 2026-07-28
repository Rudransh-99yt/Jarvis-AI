from voice.listen import record
from voice.transcribe import transcribe
from brain.chat import ask_ai
from voice.speak import speak

WAKE_WORD = "hey jarvis"

print("🤖 Jarvis is running... Say 'Hey Jarvis'")

while True:
    record()

    text = transcribe().strip().lower()

    if not text:
        continue

    print(f"You: {text}")

    if not text.startswith(WAKE_WORD):
        print("😴 Wake word not detected.")
        continue

    query = text[len(WAKE_WORD):].strip()

    if not query:
        speak("Yes?")
        continue

    reply = ask_ai(query)
    speak(reply)
