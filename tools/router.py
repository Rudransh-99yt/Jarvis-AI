import re

def needs_tools(text):
    text = text.lower()

    patterns = [
        r"\bopen\b",
        r"\bclose\b",
        r"\bquit\b",
        r"\bsearch\b",
        r"\bgoogle\b",
        r"\btime\b",
        r"\bdate\b",
        r"\btimer\b",
        r"\bvolume\b",
        r"\bbrightness\b",
        r"\bcalculator\b",
        r"\bcalculate\b",
        r"\bscreenshot\b",
        r"\bremember\b",
        r"\bshutdown\b",
        r"\brestart\b",
        r"\bsleep\b",
        r"\block\b",
    ]

    return any(re.search(p, text) for p in patterns)
