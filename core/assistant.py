from voice.live import record
from voice.transcribe import transcribe
from voice.speak import speak

from agent.planner import plan
from agent.executor import execute
from llm.mlx_engine import ask as ask_ai
from tools.router import needs_tools

WAKE_WORD = "jarvis"

def run():
    print("🤖 Jarvis started.")

    while True:
        record()

        text = transcribe("voice/input.wav").strip()

        if not text:
            continue

        print(f"\n👤 {text}")

        lower = text.lower()

        if WAKE_WORD in lower:
            command = lower.split(WAKE_WORD,1)[1].strip()
        else:
            command = text

        tool_calls = []

        if needs_tools(command):
            tool_calls = plan(command)

        if tool_calls:
            results = execute(tool_calls)

            prompt = f"""
User:
{command}

Tool Results:
{results}

Answer the user naturally using the tool results.
"""

            reply = ask_ai(prompt)

        else:
            reply = ask_ai(command)

        print(f"\n🤖 {reply}")
        speak(reply)

if __name__ == "__main__":
    run()
