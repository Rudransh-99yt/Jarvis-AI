import re
from memory.profile import remember, recall, forget

def process(text):
    t = text.strip()

    m = re.search(r"(?:remember|save)\s+(?:that\s+)?my\s+(.+?)\s+is\s+(.+)", t, re.I)
    if m:
        remember(m.group(1), m.group(2))
        return f"I'll remember your {m.group(1)}."

    m = re.search(r"(?:what|tell me)\s+(?:is\s+)?my\s+(.+)", t, re.I)
    if m:
        value = recall(m.group(1))
        if value:
            return value
        return "I don't know that yet."

    m = re.search(r"forget\s+my\s+(.+)", t, re.I)
    if m:
        forget(m.group(1))
        return f"I forgot your {m.group(1)}."

    return None
