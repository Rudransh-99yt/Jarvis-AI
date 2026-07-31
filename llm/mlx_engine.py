from mlx_lm import load, generate

MODEL = "mlx-community/gemma-3-4b-it-4bit"

print("Loading MLX model...")
model, tokenizer = load(MODEL)
print("Model loaded!")

def ask(prompt):
    return generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=80,
        verbose=False,
    )
