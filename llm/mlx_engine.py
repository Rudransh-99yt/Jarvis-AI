from pathlib import Path

from mlx_lm import load, generate
from memory.chat import add, context

MODEL = "mlx-community/Qwen3-8B-4bit"

SYSTEM = Path("prompts/system.txt").read_text()

print("Loading MLX model...")
model, tokenizer = load(MODEL)
print("Model loaded!")


def ask(prompt):
    add("User", prompt)

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": context() + "\n\n" + prompt},
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )

    text = generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=200,
        verbose=False,
    ).strip()

    add("Assistant", text)

    return text
