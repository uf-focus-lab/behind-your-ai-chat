from lib.chat import ask, complete, show

SYSTEM_PROMPT = """
You are a helpful assistant.
"""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

while (question := ask()) is not None:
    messages.append({"role": "user", "content": question})
    response = complete(messages)
    messages.append(show(response))
