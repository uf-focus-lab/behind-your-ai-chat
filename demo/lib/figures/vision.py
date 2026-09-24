"""The numbers behind the "seeing" chat slides: one photograph sent to the hosted model.

  .venv/bin/python demo/lib/figures/vision.py

Sends dog_a.jpg with "What is in the picture?" to the model chat.py uses, and
writes slides/assets/vlfm/stream-vision.json: the question and the reply as token chips, and how
many tokens the picture itself cost, measured as the difference in prompt
tokens between the request with the picture and the same request without it.
"""
import base64
import json
import os
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT.parent / "slides" / "assets" / "vlfm"
sys.path.insert(0, str(ROOT))
from lib.paths import WEIGHTS  # noqa: E402, also points HF_HUB_CACHE at lib/weights
from transformers import AutoTokenizer  # noqa: E402
from PIL import Image, ImageOps  # noqa: E402
import lib.chat as hosted  # noqa: E402

TOKENIZER = "HuggingFaceTB/SmolLM2-135M-Instruct"
from lib.paths import IMAGES  # noqa: E402

IMAGE = IMAGES / "dog_a.jpg"
QUESTION = "What is in the picture?"
SYSTEM = {"role": "system", "content": "You are a helpful assistant."}

b64 = base64.b64encode(IMAGE.read_bytes()).decode()
with_image = [SYSTEM, {"role": "user", "content": [
    {"type": "text", "text": QUESTION},
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}]
text_only = [SYSTEM, {"role": "user", "content": QUESTION}]

api = hosted.client()
seen = api.chat.completions.create(model=hosted.MODEL, messages=with_image, reasoning_effort="none")
blind = api.chat.completions.create(model=hosted.MODEL, messages=text_only, reasoning_effort="none", max_completion_tokens=16)
reply = seen.choices[0].message.content
image_tokens = seen.usage.prompt_tokens - blind.usage.prompt_tokens

tok = AutoTokenizer.from_pretrained(TOKENIZER)
chips = lambda text: [{"token": tok.decode([i]), "id": i} for i in tok(text)["input_ids"]]  # noqa: E731
ImageOps.fit(Image.open(IMAGE), (392, 392)).save(OUT / "dog_a-square.webp", quality=88)
(OUT / "stream-vision.json").write_text(json.dumps({
    "model": hosted.MODEL, "tokenizer": TOKENIZER, "image": "dog_a-square.webp", "image_tokens": image_tokens,
    "question": chips(QUESTION), "reply": chips(reply),
}, indent=2, ensure_ascii=False))
print(f"reply: {reply}\npicture: {image_tokens} tokens")
