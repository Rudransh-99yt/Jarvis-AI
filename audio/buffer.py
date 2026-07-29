from collections import deque
from audio.config import ROLLING_BLOCKS

class RollingBuffer:
    def __init__(self):
        self.buffer = deque(maxlen=ROLLING_BLOCKS)

    def add(self, chunk):
        self.buffer.append(chunk.copy())

    def clear(self):
        self.buffer.clear()

    def get(self):
        return list(self.buffer)

    def __len__(self):
        return len(self.buffer)
