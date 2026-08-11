
import time

print("Testing persistent runtime...")

t = time.time()

from brain.runtime import LLM, TOKENIZER, STT, TTS

print()
print("========================================")
print("RUNTIME TEST")
print("========================================")

print("LLM:", type(LLM).__name__)
print("TOKENIZER:", type(TOKENIZER).__name__)
print("STT:", type(STT).__name__)
print("TTS:", type(TTS).__name__)

print()
print(f"Runtime import/load: {time.time() - t:.2f}s")
print("✅ Persistent runtime works.")
