import subprocess
import re

SAFE = {
    "pwd",
    "ls",
    "whoami",
    "date",
    "uptime",
    "df -h",
    "free",
    "uname -a",
    "ifconfig",
    "ipconfig",
}

def run(text):
    cmd = re.sub(r"^(run|execute|terminal|cmd)\s*", "", text, flags=re.I).strip()

    if cmd not in SAFE:
        return "Command not allowed."

    try:
        out = subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.STDOUT,
            text=True
        )
        return out[:4000] if out else "Done."
    except Exception as e:
        return str(e)
