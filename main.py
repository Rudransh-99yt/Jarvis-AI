import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from voice.live import record
from voice.transcribe import transcribe
from voice.speak import speak

from brain.chat import ask_ai
from agent.planner import plan

from tools.open_app import run as open_app
from tools.calculator import run as calculator
from tools.system import run as system_tool
from tools.screenshot import run as screenshot_tool
from tools.web_search import run as web_search
from tools.time_tool import run as time_tool
from tools.timer import run as timer_tool
from tools.clipboard import run as clipboard_tool
from tools.memory import run as memory_tool
from tools.volume import run as volume_tool
from tools.brightness import run as brightness_tool

TOOLS = {
    "open_app": open_app,
    "calculator": calculator,
    "system": system_tool,
    "screenshot": screenshot_tool,
    "web_search": web_search,
    "time": time_tool,
    "timer": timer_tool,
    "clipboard": clipboard_tool,
    "memory": memory_tool,
    "volume": volume_tool,
    "brightness": brightness_tool,
}

print("🤖 Jarvis is ready.")

while True:
    record()
    text = transcribe("voice/input.wav").strip()

    if not text:
        continue

    print(f"\n👤 {text}")

    tasks = plan(text)

    if tasks:
        replies = []
        for tool, cmd in tasks:
            try:
                replies.append(TOOLS[tool](cmd))
            except Exception as e:
                replies.append(f"{tool}: {e}")

        reply = "\n".join(replies)
    else:
        reply = ask_ai(text)

    print(f"\n🤖 {reply}")
    speak(reply)
