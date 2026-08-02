from tools import TOOLS

def execute(tool_calls):
    outputs=[]

    for call in tool_calls:
        name=call["tool"]
        args=call.get("args","")

        if name not in TOOLS:
            outputs.append({
                "tool":name,
                "result":"Unknown tool."
            })
            continue

        try:
            result=TOOLS[name](args)
        except Exception as e:
            result=str(e)

        outputs.append({
            "tool":name,
            "result":result
        })

    return outputs
