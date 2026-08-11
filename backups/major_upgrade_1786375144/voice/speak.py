import subprocess

VOICE = "Samantha"

_process = None


def stop():
    global _process

    if _process and _process.poll() is None:
        _process.terminate()

    _process = None


def is_speaking():
    return _process is not None and _process.poll() is None


def wait_until_done():
    global _process

    if _process:
        _process.wait()
        _process = None


def speak(text):
    global _process

    stop()

    _process = subprocess.Popen([
        "say",
        "-v",
        VOICE,
        "-r",
        "220",
        text
    ])

    print("🔊 TTS started")
