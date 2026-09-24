# Behind Your AI Chat

A tour of LLMs, agentic AI and vision-language foundation models, given as a guest lecture in EEL 4403 / 5406 Computational Photography at the University of Florida, Fall 2026.

Everything you type into a chat window becomes one stream of tokens, and everything the model does is predict the next one. The lecture starts from that window and takes it apart: the stream the model actually reads, the system prompt nobody typed, and the loop that turns a chatbot into an agent, built live in a Python program short enough to fit on a slide, which grows tools in front of the class. Then the same trick for pictures: a photograph enters the stream as 1 185 tokens, CLIP puts sentences and pictures in one space, the class fights over the best caption for a photo taken in the room, and a robot from our lab finds its way through a building on nothing but CLIP vectors and sentences. It ends where the day's lab begins.

Slides: [uf-focus-lab.github.io/behind-your-ai-chat](https://uf-focus-lab.github.io/behind-your-ai-chat/), built from `slides/` by the workflow in this repository. A recording will be linked here after the lecture.

## Run the demos

Two programs under `demo/`, each one screen long, on a laptop CPU with Python 3.12.

```sh
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd demo
python chat.py                  # a shell around a chat model; add tools with @tool from lib/tool.py
python clip.py photo.jpg        # the caption contest: type "a caption # group", CLIP scores it
```

`chat.py` needs an API key: put `OPENAI_API_KEY=…` and `OPENAI_MODEL=…` in a file named `.env` in `demo/` and `chmod 600` it; git ignores it and nothing printed contains it. Model weights download on first use into `demo/lib/weights/`, or ahead of time with `python -m lib.fetch_weights`. The scripts in `demo/lib/figures/` recompute every picture in the deck into `slides/assets/`.

## Credits and licences

The code is the course's own. Models: SmolLM2-135M-Instruct and DINOv2 ViT-S/14, Apache 2.0; CLIP ViT-B/32, MIT code with weights for research and classroom use; the chat model through the OpenAI API. The four photographs under `demo/lib/images/` are CC0 from Wikimedia Commons by Johan Spaedtke, George E. Koronaios, Alexandru Stavrica and Ryan Holloway. The ChatGPT, Claude, Gemini and Grok marks on the agents slide come from Wikimedia Commons, public domain or CC0 as simple marks, and remain trademarks of their owners, used only to identify the products. The VL-Explore brief video is the lecturer's own. The deck is built with Slidev, MIT.
