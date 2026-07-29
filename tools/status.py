import subprocess

def run(text):
    text = text.lower()

    if "battery" in text:
        out = subprocess.check_output(["pmset", "-g", "batt"]).decode()
        return out.split("\n")[1].strip()

    if "wifi" in text:
        out = subprocess.check_output(["networksetup", "-getairportpower", "en0"]).decode()
        return out.strip()

    return "Unknown status command."
