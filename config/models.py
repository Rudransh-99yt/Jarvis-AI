
# All heavyweight models are loaded ONCE and kept resident.

LLM_MODEL = "mlx-community/Qwen3-4B-4bit"

STT_MODEL = "mlx-community/parakeet-tdt-0.6b-v3"

TTS_MODEL = "mlx-community/Qwen3-TTS-12Hz-0.6B-Base-4bit"

# Short answers make Jarvis dramatically faster.
LLM_MAX_TOKENS = 180

# We explicitly disable long reasoning for ordinary assistant actions.
ENABLE_THINKING = False
