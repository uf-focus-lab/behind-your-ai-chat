from lib.chat import ask, complete, show

SYSTEM_PROMPT = """
You are a helpful assistant.
"""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

while (question := ask(messages)) is not None:
    messages.append({"role": "user", "content": question})
    reply = complete(messages)
    show(reply)
    messages.append(reply)
