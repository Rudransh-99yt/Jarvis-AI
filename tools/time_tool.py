from datetime import datetime

def run(_):
    return datetime.now().strftime("It is %I:%M %p.")
