"""Download every model once, so the demos run with the network off.

  python -m lib.fetch_weights
"""
from huggingface_hub import snapshot_download
from lib.paths import WEIGHTS

MODELS = [
    "openai/clip-vit-base-patch32",        # clip.py
    "facebook/dinov2-small",               # lib/figures/dino.py, the DINO slide
    "HuggingFaceTB/SmolLM2-135M-Instruct",  # lib/figures/llm.py
]

for repo in MODELS:
    path = snapshot_download(repo, ignore_patterns=["*.h5", "*.msgpack", "*.bin", "*.onnx*", "*openvino*", "*.tflite"])
    print(f"{repo:40s} {path}")
print(f"\nweights live under {WEIGHTS}")
