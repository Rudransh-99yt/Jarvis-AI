import subprocess

VOICE = "Samantha"

def speak(text):
    subprocess.run([
        "say",
        "-v",
        VOICE,
        "-r",
        "190",
        text
    ])
