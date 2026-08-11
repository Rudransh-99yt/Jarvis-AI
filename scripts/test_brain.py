
from brain.jarvis_brain import think

tests = [
    "open WhatsApp",
    "please launch Discord and Antigravity",
    "what time is it?",
    "set the volume to 80 percent",
    "tell me a short joke",
]

for text in tests:
    print()
    print("=" * 60)
    print("USER:", text)

    result = think(text)

    print("RESULT:", result)
