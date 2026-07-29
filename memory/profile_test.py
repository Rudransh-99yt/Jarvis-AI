import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from memory.profile import remember, recall

remember("favorite_color", "blue")
print(recall("favorite_color"))

remember("city", "Delhi")
print(recall("city"))

print("✅ Persistent Memory Works")
