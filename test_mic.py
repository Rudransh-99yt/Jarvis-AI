from voice.mic import start, stop, read

start()

for i in range(10):
    read()
    print(i)

stop()

print("Done ✅")
