import subprocess

def run(_):
    path = "/Users/$USER/Desktop/screenshot.png"
    subprocess.run(f"screencapture '{path}'", shell=True)
    return "Screenshot taken."
