import numpy as np
from voice.recorder import Recorder

r = Recorder()

for _ in range(20):
    r.add(np.zeros((512,1), dtype=np.float32))

print(len(r.frames))

r.clear()

print(len(r.frames))
