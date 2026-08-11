from pathlib import Path
import shutil
import time

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "backups" / f"major_upgrade_{int(time.time())}"
BACKUP.mkdir(parents=True, exist_ok=True)

def backup(path):
    p = ROOT / path
    if p.exists():
        dest = BACKUP / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)
        print(f"BACKUP  {path}")

def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    print(f"WRITE   {path}")

print("=" * 70)
print("JARVIS MAJOR PERFORMANCE UPGRADE")
print("=" * 70)

# ------------------------------------------------------------
# BACKUPS
# ------------------------------------------------------------

for f in [
    "core/assistant.py",
    "voice/transcribe.py",
    "voice/speak.py",
    "llm/mlx_engine.py",
    "agent/planner.py",
    "agent/executor.py",
    "tools/__init__.py",
]:
    backup(f)

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

write("config/models.py", r'''
# All heavyweight models are loaded ONCE and kept resident.

LLM_MODEL = "mlx-community/Qwen3-4B-4bit"

STT_MODEL = "mlx-community/parakeet-tdt-0.6b-v3"

TTS_MODEL = "mlx-community/Qwen3-TTS-12Hz-0.6B-Base-4bit"

# Short answers make Jarvis dramatically faster.
LLM_MAX_TOKENS = 180

# We explicitly disable long reasoning for ordinary assistant actions.
ENABLE_THINKING = False
''')

# ------------------------------------------------------------
# MODEL RUNTIME
# ------------------------------------------------------------

write("brain/runtime.py", r'''
"""
Persistent Jarvis model runtime.

The important idea:
    load once
    reuse forever

This prevents every question from rebuilding/loading model objects.
"""

import time

from config.models import (
    LLM_MODEL,
    STT_MODEL,
    TTS_MODEL,
)

print("========================================")
print("Loading Jarvis AI runtime...")
print("========================================")

_t0 = time.time()

# -------------------------
# LLM
# -------------------------

print("🧠 Loading Qwen3-4B...")
from mlx_lm import load as mlx_load

LLM, TOKENIZER = mlx_load(LLM_MODEL)

print(f"✅ LLM ready in {time.time() - _t0:.2f}s")

# -------------------------
# STT
# -------------------------

_t1 = time.time()

print("🎤 Loading Parakeet...")

from mlx_audio.stt import load as load_stt

STT = load_stt(STT_MODEL)

print(f"✅ STT ready in {time.time() - _t1:.2f}s")

# -------------------------
# TTS
# -------------------------

_t2 = time.time()

print("🔊 Loading Qwen TTS...")

from mlx_audio.tts.utils import load_model as load_tts

TTS = load_tts(TTS_MODEL)

print(f"✅ TTS ready in {time.time() - _t2:.2f}s")

print("========================================")
print(f"🚀 ALL MODELS READY")
print(f"🚀 Total startup: {time.time() - _t0:.2f}s")
print("========================================")
''')

# ------------------------------------------------------------
# FAST STT
# ------------------------------------------------------------

write("voice/fast_transcribe.py", r'''
import time

from brain.runtime import STT


def transcribe(audio_path):
    t = time.time()

    result = STT.generate(audio_path)

    text = getattr(result, "text", str(result)).strip()

    elapsed = time.time() - t

    print(f"📝 Parakeet: {elapsed:.2f}s")
    print(f"👤 {text}")

    return text
''')

# ------------------------------------------------------------
# FAST TTS
# ------------------------------------------------------------

write("voice/fast_speak.py", r'''
import subprocess
import tempfile
import time
from pathlib import Path

from brain.runtime import TTS


def speak(text):
    """
    Generate speech using the already-loaded Qwen TTS model.

    We intentionally don't launch mlx-audio's CLI for every response.
    """

    text = str(text).strip()

    if not text:
        return

    t = time.time()

    output_dir = Path(tempfile.mkdtemp(prefix="jarvis_tts_"))

    results = list(
        TTS.generate(
            text=text,
            language="English",
        )
    )

    if not results:
        print("⚠️ TTS returned no audio")
        return

    audio = results[0].audio
    sample_rate = results[0].sample_rate

    output_file = output_dir / "reply.wav"

    try:
        import soundfile as sf
        sf.write(str(output_file), audio, sample_rate)

        subprocess.run(
            ["afplay", str(output_file)],
            check=False,
        )

    finally:
        try:
            output_file.unlink(missing_ok=True)
            output_dir.rmdir()
        except Exception:
            pass

    print(f"🔊 TTS: {time.time() - t:.2f}s")
''')

# ------------------------------------------------------------
# SINGLE BRAIN
# ------------------------------------------------------------

write("brain/jarvis_brain.py", r'''
"""
Single-model Jarvis brain.

There is NO separate planner LLM.

Qwen itself decides:
    conversation
    OR
    tool execution

The tool protocol is intentionally simple.
"""

import json
import re
import time

from mlx_lm import generate

from brain.runtime import LLM, TOKENIZER
from config.models import LLM_MAX_TOKENS


SYSTEM = r"""
You are Jarvis, a fast local Mac assistant.

You have tools.

IMPORTANT:
Return ONLY one JSON object.

For a normal conversation:
{"type":"answer","text":"..."}

For an action:
{"type":"tool","tool":"TOOL_NAME","args":"..."}

For multiple actions:
{"type":"tools","calls":[
  {"tool":"TOOL_NAME","args":"..."},
  {"tool":"TOOL_NAME","args":"..."}
]}

Available tools:

open_app(text)
close_app(text)
web_search(text)
calculator(text)
time(text)
timer(text)
volume(text)
brightness(text)
system(text)
memory(text)
screenshot(text)

Examples:

User: launch WhatsApp
{"type":"tool","tool":"open_app","args":"WhatsApp"}

User: could you fire up Discord and Antigravity?
{"type":"tools","calls":[
  {"tool":"open_app","args":"Discord"},
  {"tool":"open_app","args":"Antigravity"}
]}

User: what time is it?
{"type":"tool","tool":"time","args":""}

User: make the volume 80 percent
{"type":"tool","tool":"volume","args":"80"}

User: hey, tell me a joke
{"type":"answer","text":"..."}

Never invent tools.
Never output markdown.
Never output explanations outside JSON.
"""


def _extract_json(text):
    text = text.strip()

    # Remove common Qwen thinking markers if they appear.
    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL,
    ).strip()

    # Find the first JSON object.
    start = text.find("{")

    if start < 0:
        return None

    depth = 0
    in_string = False
    escaped = False

    for i in range(start, len(text)):
        c = text[i]

        if escaped:
            escaped = False
            continue

        if c == "\\":
            escaped = True
            continue

        if c == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if c == "{":
            depth += 1

        elif c == "}":
            depth -= 1

            if depth == 0:
                candidate = text[start:i + 1]

                try:
                    return json.loads(candidate)
                except Exception:
                    return None

    return None


def think(user_text):
    prompt = TOKENIZER.apply_chat_template(
        [
            {
                "role": "system",
                "content": SYSTEM,
            },
            {
                "role": "user",
                "content": user_text,
            },
        ],
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )

    t = time.time()

    raw = generate(
        LLM,
        TOKENIZER,
        prompt=prompt,
        max_tokens=LLM_MAX_TOKENS,
        verbose=False,
    )

    elapsed = time.time() - t

    result = _extract_json(raw)

    print(f"🧠 Brain: {elapsed:.2f}s")

    if result is None:
        print("⚠️ Brain JSON failed.")
        print("Raw:", raw)
        return {
            "type": "answer",
            "text": raw.strip(),
        }

    return result
''')

# ------------------------------------------------------------
# TOOL BRIDGE
# ------------------------------------------------------------

write("brain/tools.py", r'''
from tools import TOOLS


def execute_one(name, args):
    if name not in TOOLS:
        return f"Unknown tool: {name}"

    try:
        return TOOLS[name](args)
    except Exception as e:
        return f"Tool error: {e}"


def execute(plan):
    kind = plan.get("type")

    if kind == "answer":
        return plan.get("text", "")

    if kind == "tool":
        return execute_one(
            plan.get("tool", ""),
            plan.get("args", ""),
        )

    if kind == "tools":
        outputs = []

        for call in plan.get("calls", []):
            outputs.append(
                execute_one(
                    call.get("tool", ""),
                    call.get("args", ""),
                )
            )

        return "\n".join(str(x) for x in outputs)

    return "I couldn't determine the requested action."
''')

# ------------------------------------------------------------
# NEW ASSISTANT LOOP
# ------------------------------------------------------------

write("core/assistant_fast.py", r'''
import time

from voice.live import record
from voice.fast_transcribe import transcribe
from voice.fast_speak import speak

from brain.jarvis_brain import think
from brain.tools import execute


def run():
    print()
    print("========================================")
    print("🤖 JARVIS FAST MODE")
    print("========================================")
    print("All AI models stay loaded.")
    print("No separate planner.")
    print("Press Ctrl+C to stop.")
    print()

    question = 0

    while True:
        question += 1

        print()
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📊 Question #{question}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        total_start = time.time()

        # -------------------------
        # RECORD
        # -------------------------

        print("🎤 Listening...")
        record()

        # -------------------------
        # STT
        # -------------------------

        text = transcribe("voice/input.wav")

        if not text:
            print("⚠️ Nothing heard.")
            continue

        # -------------------------
        # BRAIN
        # -------------------------

        plan = think(text)

        print("🧩 Decision:", plan)

        # -------------------------
        # EXECUTE / ANSWER
        # -------------------------

        result = execute(plan)

        print(f"🤖 {result}")

        # -------------------------
        # TTS
        # -------------------------

        speak(result)

        print(
            f"🚀 TOTAL: "
            f"{time.time() - total_start:.2f}s"
        )
''')

# ------------------------------------------------------------
# MAIN ENTRYPOINT
# ------------------------------------------------------------

write("main_fast.py", r'''
from core.assistant_fast import run

if __name__ == "__main__":
    run()
''')

# ------------------------------------------------------------
# SIMPLE MODEL TEST
# ------------------------------------------------------------

write("scripts/test_runtime.py", r'''
import time

print("Testing persistent runtime...")

t = time.time()

from brain.runtime import LLM, TOKENIZER, STT, TTS

print()
print("========================================")
print("RUNTIME TEST")
print("========================================")

print("LLM:", type(LLM).__name__)
print("TOKENIZER:", type(TOKENIZER).__name__)
print("STT:", type(STT).__name__)
print("TTS:", type(TTS).__name__)

print()
print(f"Runtime import/load: {time.time() - t:.2f}s")
print("✅ Persistent runtime works.")
''')

# ------------------------------------------------------------
# BRAIN TEST
# ------------------------------------------------------------

write("scripts/test_brain.py", r'''
from brain.jarvis_brain import think

tests = [
    "open WhatsApp",
    "please launch Discord and Antigravity",
    "what time is it?",
    "set the volume to 80 percent",
    "tell me a short joke",
]

for text in tests:
    print()
    print("=" * 60)
    print("USER:", text)

    result = think(text)

    print("RESULT:", result)
''')

print()
print("=" * 70)
print("FILES CREATED")
print("=" * 70)

for p in [
    "config/models.py",
    "brain/runtime.py",
    "brain/jarvis_brain.py",
    "brain/tools.py",
    "voice/fast_transcribe.py",
    "voice/fast_speak.py",
    "core/assistant_fast.py",
    "main_fast.py",
    "scripts/test_runtime.py",
    "scripts/test_brain.py",
]:
    print("✓", p)

print()
print("BACKUPS:", BACKUP)
print()
print("Upgrade files are ready.")
