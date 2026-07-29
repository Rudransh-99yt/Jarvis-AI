import subprocess

def run(text):
    text = text.lower()

    if "copy" in text:
        subprocess.run("pbcopy < voice/input.wav", shell=True)
        return "Copied."

    if "paste" in text:
        subprocess.run(["osascript","-e",'tell application "System Events" to keystroke "v" using command down'])
        return "Pasted."

    return "Clipboard command not found."
