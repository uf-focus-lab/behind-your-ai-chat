"""A caption contest with CLIP: each group types a caption for one photograph, the closest wins."""
import sys
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor
from lib.board import Board
from lib.paths import IMAGES, ROOT

MODEL = "openai/clip-vit-base-patch32"
path = sys.argv[1] if len(sys.argv) > 1 else IMAGES / "dog_a.jpg"

torch.set_grad_enabled(False)
model = CLIPModel.from_pretrained(MODEL).eval()
proc = CLIPProcessor.from_pretrained(MODEL)
unit = lambda v: v / v.norm(dim=-1, keepdim=True)  # noqa: E731

def see(image):  # one photograph -> 1 x 512
    return unit(model.get_image_features(**proc(images=image, return_tensors="pt")).pooler_output)

def read(text):  # one sentence -> 1 x 512, the same space
    return unit(model.get_text_features(**proc(text=text, truncation=True, return_tensors="pt")).pooler_output)

picture = see(Image.open(path))
score = lambda caption: float(picture @ read(caption).T)  # cosine, both unit length  # noqa: E731

Board(score, title=f"CLIP caption contest · {path} · caption # group", log=ROOT.parent / "log.txt").run()
