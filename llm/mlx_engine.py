from pathlib import Path

from mlx_lm import load, generate
from memory.chat import add, context

MODEL = "mlx-community/gemma-3-4b-it-4bit"

SYSTEM = Path("prompts/system.txt").read_text()

print("Loading MLX model...")
model, tokenizer = load(MODEL)
print("Model loaded!")

def ask(prompt):
    add("User", prompt)

    full_prompt = f"""{SYSTEM}

{context()}

Assistant:"""

    text = generate(
        model,
        tokenizer,
        prompt=full_prompt,
        max_tokens=120,
        verbose=False,
    )

    text = text.replace("</h1>", "").strip()

    add("Assistant", text)

    return text
