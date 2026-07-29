from pathlib import Path
import re

def installed_apps():
    apps = {}

    for folder in [
        "/Applications",
        "/System/Applications",
        str(Path.home() / "Applications"),
    ]:
        p = Path(folder)

        if not p.exists():
            continue

        for app in p.glob("*.app"):
            name = re.sub(r"[^\w\s.+-]", "", app.stem.lower()).strip()
            apps[name] = app.stem

    return apps
