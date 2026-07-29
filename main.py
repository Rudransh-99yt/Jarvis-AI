import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from voice.live import record
from voice.transcribe import transcribe
from voice.speak import speak

from brain.chat import ask_ai

from tools.router import route
from tools.open_app import run as open_app
from tools.calculator import run as calculator
from tools.system import run as system_tool
from tools.screenshot import run as screenshot_tool

print("🤖 Jarvis is ready.")

while True:
    record()

    text = transcribe("voice/input.wav").strip()

    if not text:
        continue

    print(f"\n👤 {text}")

    tool = route(text)

    if tool == "open_app":
        reply = open_app(text)

    elif tool == "calculator":
        reply = calculator(text)

    elif tool == "system":
        reply = system_tool(text)

    elif tool == "screenshot":
        reply = screenshot_tool(text)

    else:
        reply = ask_ai(text)

    print(f"\n🤖 {reply}")

    speak(reply)
from tools.system import run as system_tool
