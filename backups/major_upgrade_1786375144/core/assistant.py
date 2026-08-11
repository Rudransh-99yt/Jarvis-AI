import csv
import time
from pathlib import Path

from voice.live import record
from voice.transcribe import transcribe
from voice.speak import speak, wait_until_done

from agent.planner import plan
from agent.executor import execute
from llm.mlx_engine import ask as ask_ai


WAKE_WORD = "jarvis"


def run():
    question_number = 0

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "performance.csv"

    if not log_file.exists():
        with open(log_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "question",
                "transcribe_seconds",
                "planner_seconds",
                "llm_seconds",
                "speak_seconds",
                "total_seconds",
            ])

    print("🤖 Jarvis started.")

    while True:
        question_number += 1
        question_start = time.time()

        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📊 Question #{question_number}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        record()

        # -------------------------
        # TRANSCRIPTION
        # -------------------------
        t1 = time.time()

        text = transcribe("voice/input.wav").strip()

        transcribe_time = time.time() - t1

        print(f"🎙️ Transcribe: {transcribe_time:.2f}s")

        if not text:
            continue

        print(f"\n👤 {text}")

        lower = text.lower()

        if WAKE_WORD in lower:
            command = lower.split(WAKE_WORD, 1)[1].strip()
        else:
            command = text

        # -------------------------
        # FAST PATH
        # -------------------------
        t2 = time.time()

        command_lower = command.lower().strip()

        fast_reply = None

        # -------------------------
        # FAST PATH
        # -------------------------
        if (
            "what time" in command_lower
            or "what's the time" in command_lower
            or "tell me the time" in command_lower
            or command_lower == "time"
        ):
            from datetime import datetime
            fast_reply = datetime.now().strftime("It is %I:%M %p.")

        elif command_lower in {"tell me a joke", "tell a joke", "joke"}:
            fast_reply = "Why did the computer go to the doctor? Because it had a virus."

        elif command_lower in {"hello", "hi", "hey", "hello jarvis", "hi jarvis", "hey jarvis"}:
            fast_reply = "Hello. How can I help?"

        elif command_lower in {"thank you", "thanks", "thanks jarvis"}:
            fast_reply = "You're welcome."


        planner_time = 0.0
        llm_time = 0.0

        if fast_reply is not None:
            reply = fast_reply
            print("⚡ FAST PATH: time")
        else:
            # -------------------------
            # PLANNER
            # -------------------------
            t2 = time.time()

            tool_calls = plan(command)

            planner_time = time.time() - t2

            print(f"🧠 Planner: {planner_time:.2f}s")

            # -------------------------
            # LLM / TOOL EXECUTION
            # -------------------------
            t3 = time.time()

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

            llm_time = time.time() - t3

            print(f"🧠 LLM: {llm_time:.2f}s")

        # -------------------------
        # SPEECH
        # -------------------------
        print(f"\n🤖 {reply}")

        t4 = time.time()

        speak(reply)

        speak_time = time.time() - t4

        # CRITICAL: do not open the microphone while TTS is speaking
        print("⏳ Waiting for Jarvis to finish speaking...")
        wait_until_done()
        print("✅ Jarvis finished speaking")

        print(f"🔊 Speak: {speak_time:.2f}s")

        # -------------------------
        # TOTAL
        # -------------------------
        total_time = time.time() - question_start

        print(f"🚀 TOTAL QUESTION TIME: {total_time:.2f}s")

        # Save performance data
        with open(log_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                question_number,
                f"{transcribe_time:.2f}",
                f"{planner_time:.2f}",
                f"{llm_time:.2f}",
                f"{speak_time:.2f}",
                f"{total_time:.2f}",
            ])

        print(f"💾 Saved performance data → {log_file}")

        time.sleep(0.6)


if __name__ == "__main__":
    run()
