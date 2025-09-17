from lib.constants import UPLOADS_PATH
from os import path, remove

def clear_cache(id: str) -> None:
    metronome_path = f"{UPLOADS_PATH}/{id}-metronome.mp3"
    if path.exists(metronome_path):
        remove(metronome_path)
        print(f"[{id}] Metronome removed")
    else:
        print(f"[{id}] Metronome was not found (?)")