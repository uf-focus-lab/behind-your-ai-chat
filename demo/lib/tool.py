"""Tools a chat model may ask for. A tool is a Python function; @tool writes the schema the model reads.

Nothing is registered until a program does so: decorate a new function with
@tool, or register the two below with tool(get_time) and tool(calculate).
Once anything is registered, lib.chat.complete offers it to the model.
"""
import ast
import datetime
import inspect
import json
import operator
import zoneinfo

TOOLS, HANDLERS = [], {}
TYPES = {str: "string", int: "integer", float: "number", bool: "boolean"}


def tool(fn):
    """Register a function: its name, docstring and type hints become the schema."""
    params = inspect.signature(fn).parameters
    TOOLS.append({"type": "function", "function": {
        "name": fn.__name__,
        "description": inspect.getdoc(fn),
        "parameters": {
            "type": "object",
            "properties": {name: {"type": TYPES[p.annotation]} for name, p in params.items()},
            "required": list(params),
        },
    }})
    HANDLERS[fn.__name__] = fn
    return fn


def run(call):
    """Run one tool call from a reply and return the message that carries its result.

    An error is a result too: the model reads it and decides what to do next.
    """
    name = call["function"]["name"]
    try:
        result = HANDLERS[name](**json.loads(call["function"]["arguments"]))
    except Exception as error:
        result = f"{type(error).__name__}: {error}"
    return {"role": "tool", "tool_call_id": call["id"], "name": name, "content": str(result)}


def get_time(zone: str):
    """Date and time in an IANA time zone, e.g. Asia/Tokyo."""
    return datetime.datetime.now(zoneinfo.ZoneInfo(zone)).strftime("%Y-%m-%d %H:%M %Z")


OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
       ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg}


def calculate(expression: str):
    """Evaluate an arithmetic expression exactly, e.g. 123456 * 789."""
    def ev(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
            return OPS[type(node.op)](ev(node.operand))
        raise ValueError("arithmetic only")
    return ev(ast.parse(expression, mode="eval").body)
