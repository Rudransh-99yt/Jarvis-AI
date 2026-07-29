def route(text: str):
    text = text.lower()

    if "timer" in text:
        return "timer"

    if "time" in text:
        return "time"

    if "search" in text or "google" in text or "find" in text or "look up" in text:
        return "web_search"

    if "open" in text:
        return "open_app"

    if "screenshot" in text:
        return "screenshot"

    if "lock" in text or "sleep" in text:
        return "system"

    if any(x in text for x in ["calculate", "+", "-", "*", "/"]):
        return "calculator"

    if "remember" in text:
        return "memory"

    if "remind" in text:
        return "reminder"

    return "chat"
