import subprocess

def run(_):
    subprocess.run(["screencapture", "-c"])
    return "Screenshot copied to clipboard."
