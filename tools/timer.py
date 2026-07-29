import subprocess
import re

WORDS = {
    "one":1,"two":2,"three":3,"four":4,"five":5,
    "six":6,"seven":7,"eight":8,"nine":9,"ten":10,
    "eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,
    "sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,"twenty":20
}

def run(text):
    text = text.lower()

    m = re.search(r'\d+', text)

    if m:
        mins = int(m.group())
    else:
        mins = None
        for word, value in WORDS.items():
            if word in text:
                mins = value
                break

    if mins is None:
        return "How many minutes?"

    script = f'''
delay {mins*60}
say "Your {mins} minute timer is finished"
display notification "{mins} minute timer finished." with title "Jarvis"
'''

    subprocess.Popen(["osascript", "-e", script])

    return f"Started a {mins} minute timer."
