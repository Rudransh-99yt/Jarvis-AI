from tools.open_app import run as open_app
from tools.web_search import run as web_search
from tools.calculator import run as calculator
from tools.system import run as system
from tools.screenshot import run as screenshot
from tools.clipboard import run as clipboard
from tools.volume import run as volume
from tools.brightness import run as brightness
from tools.timer import run as timer
from tools.time_tool import run as time_tool
from tools.memory import run as memory

TOOLS = {
    "open_app": open_app,
    "web_search": web_search,
    "calculator": calculator,
    "system": system,
    "screenshot": screenshot,
    "clipboard": clipboard,
    "volume": volume,
    "brightness": brightness,
    "timer": timer,
    "time": time_tool,
    "memory": memory,
}

def execute(tasks):
    results = []

    for tool, command in tasks:
        try:
            reply = TOOLS[tool](command)
            results.append(f"✓ {reply}")
        except Exception as e:
            results.append(f"✗ {tool}: {e}")

    return "\n".join(results)
