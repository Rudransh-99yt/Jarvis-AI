from collections import deque

history = deque(maxlen=12)

def add(role, text):
    history.append({"role": role, "text": text})

def context():
    return "\n".join(f'{m["role"]}: {m["text"]}' for m in history)

def clear():
    history.clear()
