def choose(prompt):
    p = prompt.lower()

    hard = [
        "code",
        "python",
        "program",
        "write",
        "essay",
        "story",
        "math",
        "explain",
        "why",
        "compare",
        "analyze",
        "research"
    ]

    for word in hard:
        if word in p:
            return "local"

    return "local"
