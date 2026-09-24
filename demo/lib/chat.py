"""The chat model behind chat.py: the key from .env, the client, and the shell's printing."""

import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLOURS = {"plain": "0", "cyan": "36", "yellow": "33"}


def load_env():
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text().splitlines():
        key, sep, value = line.partition("=")
        if sep and not line.startswith("#") and value.strip():
            os.environ.setdefault(key.strip(), value.strip())


load_env()
MODEL = os.environ.get("OPENAI_MODEL", "gpt-6-astra")


def client():
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit(
            "no API key: fill in OPENAI_API_KEY in .env at the repository root"
        )
    from openai import OpenAI

    return OpenAI()


def complete(messages):
    """One reply from the model. Once anything is registered with @tool in
    lib.tool, the model may call it: every call it makes is run, shown, and
    appended to the messages before it is asked again; the final reply comes
    back and is not appended."""
    from lib.tool import TOOLS, run
    while True:
        extra = {"tools": TOOLS} if TOOLS else {}
        reply = client().chat.completions.create(model=MODEL, messages=messages, reasoning_effort="none", **extra)
        reply = reply.choices[0].message.model_dump(exclude_none=True)
        if "tool_calls" not in reply:
            return reply
        messages.append(show(reply))
        for call in reply["tool_calls"]:
            messages.append(show(run(call)))


def rule():
    """A dim horizontal rule across the terminal, in the box-drawing character made for it."""
    print(f"\033[2m{'─' * shutil.get_terminal_size().columns}\033[0m", flush=True)


def ask(messages=None, prompt="> "):
    """One line from the user, or None when the shell is closed.

    Lines starting with a slash are commands for the shell itself: /messages
    (or /msg, /message) prints the history so far, /tools lists the registered
    tools. A line starting with ! runs in the system shell."""
    while True:
        rule()
        try:
            msg = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if msg.startswith("!"):
            rule()
            subprocess.run(msg[1:], shell=True, cwd=ROOT)
        elif msg in ("/msg", "/message", "/messages"):
            history(messages or [])
        elif msg == "/tools":
            tools()
        elif msg:
            return msg


ROLES = {"system": ("system", "2"), "user": ("user", "0"), "assistant": ("agent", "36"), "tool": ("tool", "33")}


def history(messages):
    """The conversation so far, one line per message: [role] content, in the role's colour."""
    rule()
    for m in messages:
        name, colour = ROLES.get(m["role"], (m["role"], "0"))
        for call in m.get("tool_calls", []):
            print(f"\033[{colour}m[{name}]\033[0m \033[33m{call['function']['name']}{call['function']['arguments']}\033[0m")
        text = (m.get("content") or "").strip()
        if text or not m.get("tool_calls"):
            print(f"\033[{colour}m[{name}]\033[0m \033[{colour}m{text}\033[0m")


def tools():
    """Every tool registered so far, with its parameters and description."""
    from lib.tool import TOOLS
    rule()
    if not TOOLS:
        print("\033[2mno tools registered\033[0m")
    for t in TOOLS:
        f = t["function"]
        params = ", ".join(f"{k}: {v['type']}" for k, v in f["parameters"]["properties"].items())
        print(f"\033[33m{f['name']}({params})\033[0m  {f['description']}")


def show(message):
    """Print one message the way the shell shows it: replies cyan, tool calls and results yellow."""
    rule()
    if message["role"] == "tool":
        print(f"\033[{COLOURS['yellow']}m-> {message['content']}\033[0m")
        return message
    for call in message.get("tool_calls", []):
        print(
            f"\033[{COLOURS['yellow']}m{call['function']['name']}{call['function']['arguments']}\033[0m"
        )
    if message.get("content"):
        print(f"\033[{COLOURS['cyan']}m{message['content']}\033[0m")
    return message
