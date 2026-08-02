import webbrowser
import re
from urllib.parse import quote_plus

def run(text):
    q = re.sub(
        r"\b(search|google|look up|find|browse|for|jarvis|please)\b",
        "",
        text,
        flags=re.I
    ).strip()

    if not q:
        return "What should I search?"

    webbrowser.open(f"https://www.google.com/search?q={quote_plus(q)}")
    return f"Searching for {q}."
