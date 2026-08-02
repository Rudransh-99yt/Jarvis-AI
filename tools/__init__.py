from tools.open_app import run as open_app
from tools.close_app import run as close_app
from tools.web_search import run as web_search
from tools.time_tool import run as time
from tools.timer import run as timer
from tools.volume import run as volume
from tools.brightness import run as brightness
from tools.calculator import run as calculator
from tools.system import run as system
from tools.memory import run as memory
from tools.screenshot import run as screenshot
from tools.files import run as files
from tools.terminal import run as terminal
from tools.browser import run as browser
from tools.system_status import run as system_status
from tools.clipboard import run as clipboard
from tools.notes import run as notes

TOOLS = {
    "open_app": open_app,
    "close_app": close_app,
    "web_search": web_search,
    "time": time,
    "timer": timer,
    "volume": volume,
    "brightness": brightness,
    "calculator": calculator,
    "system": system,
    "memory": memory,
     "screenshot": screenshot,
    "files": files,
    "terminal": terminal,
    "browser": browser,
    "system_status": system_status,
    "clipboard": clipboard,
    "notes": notes,
}
