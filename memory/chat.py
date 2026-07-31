history = []

def add(role, text):
    history.append((role, text))

    if len(history) > 10:
        history.pop(0)

def context():
    return "\n".join(
        f"{role}: {text}"
        for role, text in history
    )
