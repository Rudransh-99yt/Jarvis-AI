import re
from memory.store import remember, recall

def run(text):
    text = text.lower()

    m = re.search(r"remember (.+?) is (.+)", text)
    if m:
        return remember(m.group(1).strip(), m.group(2).strip())

    m = re.search(r"(what is|who is|what's) (.+)", text)
    if m:
        ans = recall(m.group(2).strip())
        return ans if ans else "I don't remember that."

    return "Memory command not found."
