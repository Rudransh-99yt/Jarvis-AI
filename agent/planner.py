import re

def plan(text):
    text = text.lower()
    tasks = []

    connectors = r"(?:and then|then|also|and|,)"

    patterns = [
        ("open_app", rf"open (.+?)(?={connectors}|$)"),
        ("web_search", rf"(?:search|google|find|look up) (.+?)(?={connectors}|$)"),
        ("volume", rf"(?:set )?volume.*?(?={connectors}|$)|mute|unmute"),
        ("brightness", rf"(?:set )?brightness.*?(?={connectors}|$)"),
        ("time", r"(?:what(?:'s| is)? the time|tell me the time|time right now)"),
        ("timer", rf"set .*?timer.*?(?={connectors}|$)"),
        ("calculator", rf"(?:calculate|what is) .+?(?={connectors}|$)")
    ]

    for tool, pattern in patterns:
        for m in re.finditer(pattern, text):
            tasks.append((m.start(), tool, m.group().strip()))

    tasks.sort(key=lambda x: x[0])

    merged = []
    for _, tool, cmd in tasks:
        if tool == "open_app":
            apps = re.split(connectors, cmd[5:])
            for app in apps:
                app = app.strip()
                if app:
                    merged.append((tool, f"open {app}"))
        else:
            merged.append((tool, cmd))

    return merged
