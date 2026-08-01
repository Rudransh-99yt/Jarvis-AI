from memory.long_term import process as memory_process
from llm.mlx_engine import ask

def think(text):
    result = memory_process(text)

    if result:
        return result

    return ask(text)
