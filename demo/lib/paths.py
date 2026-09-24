"""Where the demos find their images and weights: beside this file."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = Path(__file__).resolve().parent
IMAGES = LIB / "images"
WEIGHTS = LIB / "weights"

os.environ.setdefault("HF_HUB_CACHE", str(WEIGHTS / "hf"))
