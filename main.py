import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from voice.live import record
from voice.transcribe import transcribe
from voice.speak import speak
from brain.chat import ask_ai
from agent.planner import plan
from agent.executor import execute

WAKE_WORD = "jarvis"

print("🤖 Jarvis is ready.")

while True:
    record()

    text = transcribe("voice/input.wav").strip()

    if not text:
        continue

    print(f"\n👤 {text}")

    lower = text.lower()

    if WAKE_WORD not in lower:
        continue

    command = lower.split(WAKE_WORD, 1)[1].strip()

    if not command:
        speak("Yes?")
        continue

    try:
        tasks = plan(command)

        if tasks:
            reply = execute(tasks)
        else:
            reply = ask_ai(command)

    except Exception:
        reply = ask_ai(command)

    print(f"\n🤖 {reply}")
    speak(reply)
