import pvporcupine

porcupine = pvporcupine.create(
    keywords=["jarvis"]
)

print("✅ Porcupine loaded")
print("Wake word:", porcupine.keywords)
