from pathlib import Path\n
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
