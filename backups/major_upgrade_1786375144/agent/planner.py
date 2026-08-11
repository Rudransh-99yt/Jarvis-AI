import json
import re

from llm.mlx_engine import model, tokenizer
from mlx_lm import generate

TOOLS = """
open_app(text)
close_app(text)
web_search(text)
calculator(text)
time()
timer(text)
volume(text)
brightness(text)
system(text)
memory(text)
screenshot()
"""

PROMPT = f"""
You are an AI planner.

Convert the user's request into one or more tool calls.

Rules:

- Return ONLY JSON.
- Never explain.
- Never use markdown.
- Multiple actions -> multiple tool calls.
- Preserve execution order.
- If conversation is enough, return [].
- Ignore small talk.

Examples:

User:
open chrome

[
  {{
    "tool":"open_app",
    "args":"chrome"
  }}
]

User:
open chrome and calculator

[
  {{
    "tool":"open_app",
    "args":"chrome"
  }},
  {{
    "tool":"open_app",
    "args":"calculator"
  }}
]

User:
close chrome then open calendar

[
  {{
    "tool":"close_app",
    "args":"chrome"
  }},
  {{
    "tool":"open_app",
    "args":"calendar"
  }}
]

User:
what time is it

[
  {{
    "tool":"time",
    "args":""
  }}
]

User:
remember my birthday is 14 april

[
  {{
    "tool":"memory",
    "args":"remember my birthday is 14 april"
  }}
]

User:
tell me a joke

[]

Available tools:

{TOOLS}
"""

def plan(user):
    prompt = tokenizer.apply_chat_template(
        [
            {"role":"system","content":PROMPT},
            {"role":"user","content":user},
        ],
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )

    out = generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=300,
        verbose=False,
    ).strip()

    m = re.search(r'\[[\s\S]*\]', out)

    if not m:
        return []

    try:
        return json.loads(m.group())
    except Exception:
        return []
