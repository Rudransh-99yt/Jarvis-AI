CHAT_MODEL = "mlx-community/gemma-3-4b-it-4bit"
CODE_MODEL = "mlx-community/Qwen2.5-Coder-7B-4bit"
GENERAL_MODEL = "mlx-community/Qwen3-8B-4bit"
REASON_MODEL = "mlx-community/Qwen3-14B-4bit"

def choose_model(prompt):
    p = prompt.lower()

    code_words = [
        "python","code","bug","debug","function","class","script",
        "java","c++","javascript","html","css","sql"
    ]

    reasoning_words = [
        "explain","why","design","architecture","compare",
        "strategy","reason","think","analyze"
    ]

    if any(w in p for w in code_words):
        return CODE_MODEL

    if any(w in p for w in reasoning_words):
        return REASON_MODEL

    return CHAT_MODEL
