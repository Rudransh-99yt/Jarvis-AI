
from tools import TOOLS


def execute_one(name, args):
    if name not in TOOLS:
        return f"Unknown tool: {name}"

    try:
        return TOOLS[name](args)
    except Exception as e:
        return f"Tool error: {e}"


def execute(plan):
    kind = plan.get("type")

    if kind == "answer":
        return plan.get("text", "")

    if kind == "tool":
        return execute_one(
            plan.get("tool", ""),
            plan.get("args", ""),
        )

    if kind == "tools":
        outputs = []

        for call in plan.get("calls", []):
            outputs.append(
                execute_one(
                    call.get("tool", ""),
                    call.get("args", ""),
                )
            )

        return "\n".join(str(x) for x in outputs)

    return "I couldn't determine the requested action."
