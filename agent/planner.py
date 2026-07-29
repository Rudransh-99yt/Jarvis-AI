import re

def plan(text):
    text = text.lower()
    tasks = []

    # ---------- OPEN APPS ----------
    if "open" in text:
        after = text.split("open",1)[1]

        stop = re.search(
            r"\b(search|google|find|look up|set|tell|what|time|volume|brightness|timer)\b",
            after,
        )

        if stop:
            after = after[:stop.start()]

        after = re.sub(r"\b(app|apps|jarvis|the)\b", "", after)

        names = re.findall(r"[a-z0-9.+-]+(?:\s+[a-z0-9.+-]+)?", after)

        for name in names:
            name = name.strip()
            if name and name not in ["and"]:
                tasks.append(("open_app", f"open {name}"))

    # ---------- SEARCH ----------
    m = re.search(r"(?:search|google|find)\s+(.+?)(?=set|tell|what|time|volume|brightness|$)", text)
    if m:
        for q in re.split(r",|\band\b", m.group(1)):
            q = q.strip()
            if q:
                tasks.append(("web_search", f"search {q}"))

    if "volume" in text or "mute" in text or "unmute" in text:
        tasks.append(("volume", text))

    if "brightness" in text:
        tasks.append(("brightness", text))

    if any(x in text for x in [
        "time right now",
        "tell me the time",
        "what's the time",
        "what is the time"
    ]):
        tasks.append(("time", text))

    return tasks
