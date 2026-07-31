import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from wake.detector import wait_for_wake
import subprocess

while True:
    wait_for_wake()
    subprocess.run(["python", "main.py"])
