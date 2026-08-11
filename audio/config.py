SAMPLE_RATE = 16000
BLOCK_SIZE = 512

# Enough context for VAD to recognize speech reliably
ROLLING_SECONDS = 0.7

# Wait longer after speech so words like "WhatsApp" aren't cut off
END_SILENCE_SECONDS = 0.7

ROLLING_BLOCKS = max(
    1,
    int(ROLLING_SECONDS * SAMPLE_RATE / BLOCK_SIZE)
)

END_SILENCE_BLOCKS = max(
    1,
    int(END_SILENCE_SECONDS * SAMPLE_RATE / BLOCK_SIZE)
)
