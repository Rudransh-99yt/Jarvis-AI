import sounddevice as sd

FS = 16000
BLOCK = 480

stream = sd.RawInputStream(
    samplerate=FS,
    blocksize=BLOCK,
    channels=1,
    dtype="int16",
)

stream.start()
print("🎤 Listening...")

try:
    while True:
        data, overflowed = stream.read(BLOCK)
        print(len(data))
except KeyboardInterrupt:
    pass

stream.stop()
stream.close()
print("Done.")
