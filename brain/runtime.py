
"""
Persistent Jarvis model runtime.

The important idea:
    load once
    reuse forever

This prevents every question from rebuilding/loading model objects.
"""

import time

from config.models import (
    LLM_MODEL,
    STT_MODEL,
    TTS_MODEL,
)

print("========================================")
print("Loading Jarvis AI runtime...")
print("========================================")

_t0 = time.time()

# -------------------------
# LLM
# -------------------------

print("🧠 Loading Qwen3-4B...")
from mlx_lm import load as mlx_load

LLM, TOKENIZER = mlx_load(LLM_MODEL)

print(f"✅ LLM ready in {time.time() - _t0:.2f}s")

# -------------------------
# STT
# -------------------------

_t1 = time.time()

print("🎤 Loading Parakeet...")

from mlx_audio.stt import load as load_stt

STT = load_stt(STT_MODEL)

print(f"✅ STT ready in {time.time() - _t1:.2f}s")

# -------------------------
# TTS
# -------------------------

_t2 = time.time()

print("🔊 Loading Qwen TTS...")

from mlx_audio.tts.utils import load_model as load_tts

TTS = load_tts(TTS_MODEL)

print(f"✅ TTS ready in {time.time() - _t2:.2f}s")

print("========================================")
print(f"🚀 ALL MODELS READY")
print(f"🚀 Total startup: {time.time() - _t0:.2f}s")
print("========================================")
