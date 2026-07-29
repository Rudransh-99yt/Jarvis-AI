import webbrowser
from urllib.parse import quote

def run(text):
    query = (
        text.lower()
        .replace("search", "")
        .replace("google", "")
        .replace("for", "").replace("find", "").replace("look up", "")
        .strip()
    )

    if not query:
        return "What should I search?"

    url = f"https://www.google.com/search?q={quote(query)}"
    webbrowser.open(url)

    return f"Searching Google for {query}."
