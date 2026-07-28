from rich.console import Console
from voice.listen import record
from voice.transcribe import transcribe
from core.assistant import ask

console = Console()

def main():
    console.print("[bold green]Jarvis Voice Test[/bold green]")

    while True:
        input("\nPress Enter to speak...")

        record()

        text = transcribe("voice/input.wav")

        console.print(f"\nYou: {text}")

        if text.lower() in {"exit", "quit"}:
            break

        reply = ask(text)

        console.print(f"\nJarvis: {reply}")

if __name__ == "__main__":
    main()
