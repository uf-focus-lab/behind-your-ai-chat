"""The numbers behind the CLIP slide: four photographs against four captions.

  .venv/bin/python demo/lib/figures/clip.py

Writes into slides/assets/vlfm/: clip-matrix.json, the cosine between every
caption and every photograph in CLIP's shared space; a square thumbnail of each
photograph; clip-patches.webp and clip-outputs.json, the vision tower's patch
vectors on the dog painted by PCA and the shapes of its two outputs; and
clip-pair.json, the one pair on the "one vector each" slide.
"""
import json
import pathlib
import sys

import torch
from PIL import Image, ImageOps
from transformers import CLIPModel, CLIPProcessor

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT.parent / "slides" / "assets" / "vlfm"
sys.path.insert(0, str(ROOT))
from lib.paths import IMAGES  # noqa: E402

MODEL = "openai/clip-vit-base-patch32"
PAIRS = [
    ("dog_a", "a golden retriever in a forest"),
    ("dog_b", "a dog resting on a red doormat"),
    ("mug_a", "a steaming yellow striped mug"),
    ("mug_b", "a white enamel mug with a skull"),
]

torch.set_grad_enabled(False)
model = CLIPModel.from_pretrained(MODEL).eval()
proc = CLIPProcessor.from_pretrained(MODEL)
unit = lambda v: v / v.norm(dim=-1, keepdim=True)  # noqa: E731

images = [Image.open(IMAGES / f"{name}.jpg") for name, _ in PAIRS]
V = unit(model.get_image_features(**proc(images=images, return_tensors="pt")).pooler_output)
T = unit(model.get_text_features(**proc(text=[c for _, c in PAIRS], padding=True, return_tensors="pt")).pooler_output)
cos = (T @ V.T).tolist()  # captions x images

for (name, _), img in zip(PAIRS, images):
    ImageOps.fit(img, (240, 240)).save(OUT / f"{name}.webp", quality=85)
(OUT / "clip-matrix.json").write_text(json.dumps({
    "model": MODEL, "dim": V.shape[1], "temperature": round(float(model.logit_scale.exp()), 1),
    "images": [n for n, _ in PAIRS], "captions": [c for _, c in PAIRS],
    "cosine": [[round(x, 3) for x in row] for row in cos],
}, indent=2))
for (_, caption), row in zip(PAIRS, cos):
    print(f"{caption:36s}" + "".join(f"{x:7.3f}" for x in row))

# region two outputs
# The same encoder, both outputs, on the dog: the 49 patch vectors coloured by
# their first three principal components, and the shapes of each output.
import numpy as np
vision = model.vision_model(**proc(images=images[0], return_tensors="pt"))
patches = vision.last_hidden_state[0, 1:]                      # 49 x 768, the class token dropped
pooled = model.visual_projection(vision.pooler_output)          # 1 x 512, what CLIP trains
x = patches.numpy() - patches.numpy().mean(axis=0)
rgb = x @ np.linalg.svd(x, full_matrices=False)[2][:3].T
lo, hi = np.percentile(rgb, 2, axis=0), np.percentile(rgb, 98, axis=0)
side = int(np.sqrt(len(patches)))
rgb = np.clip((rgb - lo) / (hi - lo), 0, 1).reshape(side, side, 3)
Image.fromarray(np.uint8(255 * rgb)).resize((392, 392), Image.NEAREST).save(OUT / "clip-patches.webp", quality=90)
(OUT / "clip-outputs.json").write_text(json.dumps({
    "model": MODEL, "grid": side, "patch_px": 224 // side,
    "patches": list(patches.shape), "pooled": list(pooled.shape), "class_width": vision.pooler_output.shape[1],
}, indent=2))
print(f"patches {tuple(patches.shape)}, pooled {tuple(pooled.shape)}, grid {side} x {side}")
# endregion

# region one pair
# The pair on the "one vector each" slide: a short caption against the dog.
CAPTION = "a dog in the woods"
tok = proc(text=CAPTION, return_tensors="pt")
t = unit(model.get_text_features(**tok).pooler_output)
(OUT / "clip-pair.json").write_text(json.dumps({
    "model": MODEL, "image": "dog_a", "caption": CAPTION,
    "tokens": int(tok["input_ids"].shape[1]), "pixels": 224, "dim": int(t.shape[1]),
    "cosine": round(float(t @ V[0]), 3),
}, indent=2))
print(f"pair: {CAPTION!r} -> {tok['input_ids'].shape[1]} tokens, cosine {float(t @ V[0]):.3f}")
# endregion
