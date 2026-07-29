def run(text):
    try:
        expr = (
            text.lower()
            .replace("calculate", "")
            .replace("what is", "")
            .replace("=", "")
            .strip()
        )

        result = eval(expr, {"__builtins__": {}})
        return str(result)

    except:
        return "Couldn't calculate."
