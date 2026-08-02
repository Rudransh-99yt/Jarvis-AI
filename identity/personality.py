def reply(text):
    t = text.lower()

    if any(x in t for x in [
        "who made you",
        "who created you",
        "who built you",
        "who developed you"
    ]):
        return "I was built by Rudransh."

    if any(x in t for x in [
        "who are you",
        "what are you",
        "your name"
    ]):
        return "I'm Jarvis, your personal AI assistant."

    if "are you chatgpt" in t:
        return "No. I'm Jarvis."

    if "are you openai" in t:
        return "No."

    if "are you claude" in t:
        return "No."

    if "are you gemini" in t:
        return "No."

    return None
