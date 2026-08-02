import subprocess

def run(_):
    try:
        batt = subprocess.check_output(["pmset","-g","batt"]).decode().splitlines()[1].strip()
    except:
        batt = "Battery unavailable"

    try:
        wifi = subprocess.check_output(
            ["networksetup","-getairportpower","en0"]
        ).decode().strip()
    except:
        wifi = "Wi-Fi unavailable"

    try:
        vol = subprocess.check_output(
            ["osascript","-e","output volume of (get volume settings)"]
        ).decode().strip()
    except:
        vol = "?"

    return f"{batt}\n{wifi}\nVolume: {vol}%"
