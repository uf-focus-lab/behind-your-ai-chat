"""The picture behind the DINO slide: DINOv2's patch vectors on the dog, painted by PCA.

  .venv/bin/python demo/lib/figures/dino.py

The same computation the CLIP script does with its own encoder, on the same
photograph, so the two colourings can sit side by side. Written into
slides/assets/vlfm/.
"""
import json
import pathlib
import sys

import numpy as np
import torch
from PIL import Image, ImageOps
from transformers import AutoImageProcessor, AutoModel

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT.parent / "slides" / "assets" / "vlfm"
sys.path.insert(0, str(ROOT))
from lib.paths import IMAGES  # noqa: E402

MODEL = "facebook/dinov2-small"
SIDE = 392  # 28 x 28 patches of 14 px
image = ImageOps.fit(Image.open(IMAGES / "dog_a.jpg"), (SIDE, SIDE))

torch.set_grad_enabled(False)
proc = AutoImageProcessor.from_pretrained(MODEL)
model = AutoModel.from_pretrained(MODEL).eval()
x = proc(images=image, return_tensors="pt", do_resize=False, do_center_crop=False)
tokens = model(**x).last_hidden_state[0, 1:]  # 784 x 384
patches = tokens.numpy() - tokens.numpy().mean(axis=0)
rgb = patches @ np.linalg.svd(patches, full_matrices=False)[2][:3].T
lo, hi = np.percentile(rgb, 2, axis=0), np.percentile(rgb, 98, axis=0)
grid = SIDE // 14
rgb = np.clip((rgb - lo) / (hi - lo), 0, 1).reshape(grid, grid, 3)
Image.fromarray(np.uint8(255 * rgb)).resize((SIDE, SIDE), Image.NEAREST).save(OUT / "dino-patches.webp", quality=90)
(OUT / "dino-outputs.json").write_text(json.dumps({"model": MODEL, "grid": grid, "patch_px": 14, "patches": list(tokens.shape)}, indent=2))
print(f"patches {tuple(tokens.shape)}, grid {grid} x {grid}")
