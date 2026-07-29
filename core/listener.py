import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from voice.listen import record
from voice.transcribe import transcribe

while True:
    record()
    text = transcribe().strip().lower()

    if text:
        print("Heard:", text)
