import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from voice.live import record
from voice.transcribe import transcribe
from voice.speak import speak
from brain.chat import ask_ai

from agent.planner import plan
from agent.executor import execute

print("🤖 Jarvis is ready.")

while True:
    record()

    text = transcribe("voice/input.wav").strip()

    if not text:
        continue

    print(f"\n👤 {text}")

    try:
        tasks = plan(text)

        if tasks:
            reply = execute(tasks)
        else:
            reply = ask_ai(text)

    except Exception:
        reply = ask_ai(text)

    print(f"\n🤖 {reply}")
    speak(reply)
