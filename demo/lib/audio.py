"""
Sounds a tool can make: a file under the demo folder, or the hosted model's voice.
play("lib/meow.mp3")            a relative path is taken from the demo folder
play(tts("Miaow, it is noon."))  speech lands in a temporary file, played, then removed
"""

import subprocess
import tempfile
from pathlib import Path

from lib.chat import client

ROOT = Path(__file__).resolve().parents[1]


def play(path):
    """Play a sound file; a relative path is under ROOT, a temporary one is removed after."""
    path = Path(path) if Path(path).is_absolute() else ROOT / path
    subprocess.run(["afplay", str(path)], check=False)
    if path.parent == Path(tempfile.gettempdir()):
        path.unlink(missing_ok=True)


def tts(content: str, voice="coral"):
    """The text as speech from the hosted model, written to a temporary file; returns its path."""
    audio = client().audio.speech.create(
        model="gpt-4o-mini-tts", voice=voice, input=content
    )
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        audio.write_to_file(f.name)
        return Path(f.name)
