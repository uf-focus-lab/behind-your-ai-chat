"""The token streams behind the LLM slides, from one small open model and the hosted one.

  .venv/bin/python demo/lib/figures/llm.py

Hosted models do not publish their tokenizer, so the slides cut text into tokens
with SmolLM2-135M-Instruct, small enough to run on a laptop CPU, and take the
replies from the model chat.py talks to. Files written into slides/assets/llm/:

  stream.json        the hello-world conversation as one token stream: system,
                     user and, when .env holds an API key, the hosted model's reply
  steps.json         greedy decoding of the reply on the small model, six steps:
                     at each one the top five candidates and the one taken
  stream-tools.json  one tool turn, made live by the hosted model with the cat
                     prompt and get_time, as the same kind of token stream
"""
import json
import os
import pathlib
import sys

import torch

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT.parent / "slides" / "assets" / "llm"
sys.path.insert(0, str(ROOT))
from lib.paths import WEIGHTS  # noqa: E402, also points HF_HUB_CACHE at lib/weights
from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa: E402
import lib.chat as hosted  # noqa: E402
import lib.tool as tools  # noqa: E402

MODEL = "HuggingFaceTB/SmolLM2-135M-Instruct"
HELLO = [{"role": "system", "content": "You are a helpful assistant. Keep replies to one sentence."},
         {"role": "user", "content": "Hello! What can you help me with?"}]

tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL).eval()
chips = lambda text: [{"token": tok.decode([i]), "id": i} for i in tok(text)["input_ids"]]  # noqa: E731

# the same request chat.py makes, so the slides show the reply the class will see
reply = hosted.complete(HELLO)["content"] if os.environ.get("OPENAI_API_KEY") else None
stream = [{"role": m["role"], "tokens": chips(m["content"])} for m in HELLO]
if reply:
    stream.append({"role": "assistant", "tokens": chips(reply)})
(OUT / "stream.json").write_text(json.dumps({"model": MODEL, "recorded": bool(reply), "stream": stream}, indent=2, ensure_ascii=False))

# the reply one token at a time: the same forward pass, the top pick appended, run again
ids = tok(tok.apply_chat_template(HELLO, tokenize=False, add_generation_prompt=True), return_tensors="pt")["input_ids"]
steps = []
for _ in range(6):
    with torch.no_grad():
        p = torch.softmax(model(input_ids=ids).logits[0, -1].float(), dim=-1)
    v, i = p.topk(5)
    steps.append({"top": [{"token": tok.decode([int(k)]), "id": int(k), "p": round(float(q), 4)} for q, k in zip(v, i)],
                  "taken": {"token": tok.decode([int(i[0])]), "id": int(i[0])}})
    ids = torch.cat([ids, i[:1].reshape(1, 1)], dim=1)
(OUT / "steps.json").write_text(json.dumps({"model": MODEL, "prefix": stream[:2], "steps": steps}, indent=2, ensure_ascii=False))
print("steps:", [s["taken"]["token"] for s in steps])

# one tool turn, live
CAT = "You are a cat. You only say miaow. Use a tool when one helps."
turn = [{"role": "system", "content": CAT}, {"role": "user", "content": "What time is it in Tokyo?"}]
tools.tool(tools.get_time)  # the one tool the cat gets
if os.environ.get("OPENAI_API_KEY"):
    turn.append(hosted.complete(turn))  # the calls it makes land in turn on the way
    schema = tools.TOOLS[0]["function"]
    compact = json.dumps({"name": schema["name"], "parameters": {k: v["type"] for k, v in schema["parameters"]["properties"].items()}}, separators=(",", ":"))
    pieces = [("system", CAT), ("tools", compact), ("user", turn[1]["content"])]
    for m in turn[2:]:
        if m["role"] == "tool":
            pieces.append(("tool", m["content"]))
        elif m.get("tool_calls"):
            pieces.append(("call", "".join(c["function"]["name"] + c["function"]["arguments"] for c in m["tool_calls"])))
        else:
            pieces.append(("assistant", m["content"]))
    (OUT / "stream-tools.json").write_text(json.dumps({"model": MODEL, "hosted": hosted.MODEL, "stream": [{"role": r, "tokens": chips(t)} for r, t in pieces]}, indent=2, ensure_ascii=False))
    print("tool turn:", [(r, t) for r, t in pieces])
