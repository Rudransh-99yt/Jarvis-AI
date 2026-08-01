from core.assistant import run_once

def run():
    print("🤖 Jarvis started.")

    while True:
        run_once()

if __name__ == "__main__":
    run()
