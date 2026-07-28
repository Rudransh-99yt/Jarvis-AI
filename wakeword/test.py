while True:
    text = input("You: ").strip().lower()

    if text.startswith("hey jarvis"):
        print("✅ Wake word detected!")
    else:
        print("😴 Ignored")
