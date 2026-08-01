import time
from mlx_lm import load, generate

MODELS = [
    "mlx-community/gemma-3-4b-it-4bit",
    "mlx-community/Qwen2.5-Coder-7B-4bit",
    "mlx-community/Qwen3-8B-4bit",
    "mlx-community/Qwen3-14B-4bit",
]

prompts = [
    p.strip()
    for p in open("benchmarks/prompts.txt").read().split("\n\n")
]

for model_name in MODELS:
    print("\n" + "=" * 70)
    print(model_name)
    print("=" * 70)

    model, tokenizer = load(model_name)

    total = 0

    for prompt in prompts:
        start = time.time()

        out = generate(
            model,
            tokenizer,
            prompt=prompt,
            max_tokens=100,
            verbose=False,
        )

        t = time.time() - start
        total += t

        print(f"{t:.2f}s | {prompt[:40]}")

    print(f"\nAverage: {total/len(prompts):.2f}s")
