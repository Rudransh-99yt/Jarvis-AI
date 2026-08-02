import subprocess

def run(text):
    t = text.lower()

    if "copy" in t:
        data = text.split("copy",1)[1].strip()
        subprocess.run(["pbcopy"], input=data.encode())
        return "Copied to clipboard."

    if "paste" in t:
        return subprocess.check_output(["pbpaste"]).decode()

    if "clear" in t:
        subprocess.run(["pbcopy"], input=b"")
        return "Clipboard cleared."

    return "Say copy, paste or clear clipboard."
