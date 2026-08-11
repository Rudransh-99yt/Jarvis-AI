
import subprocess
import tempfile
import time
from pathlib import Path

from brain.runtime import TTS


def speak(text):
    """
    Generate speech using the already-loaded Qwen TTS model.

    We intentionally don't launch mlx-audio's CLI for every response.
    """

    text = str(text).strip()

    if not text:
        return

    t = time.time()

    output_dir = Path(tempfile.mkdtemp(prefix="jarvis_tts_"))

    results = list(
        TTS.generate(
            text=text,
            language="English",
        )
    )

    if not results:
        print("⚠️ TTS returned no audio")
        return

    audio = results[0].audio
    sample_rate = results[0].sample_rate

    output_file = output_dir / "reply.wav"

    try:
        import soundfile as sf
        sf.write(str(output_file), audio, sample_rate)

        subprocess.run(
            ["afplay", str(output_file)],
            check=False,
        )

    finally:
        try:
            output_file.unlink(missing_ok=True)
            output_dir.rmdir()
        except Exception:
            pass

    print(f"🔊 TTS: {time.time() - t:.2f}s")
