import sounddevice as sd

SAMPLE_RATE = 16000
BLOCK_SIZE = 512

stream = sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    blocksize=BLOCK_SIZE,
    dtype="float32",
)

def start():
    stream.start()

def stop():
    stream.stop()
    stream.close()

def read():
    data, _ = stream.read(BLOCK_SIZE)
    return data
