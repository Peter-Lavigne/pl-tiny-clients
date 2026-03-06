from pathlib import Path

from pl_tiny_clients.play_sound_raw import play_sound_raw
from pl_tiny_clients.set_volume import set_volume


def play_sound(absolute_file_path: Path, volume: int) -> None:
    set_volume(volume)
    play_sound_raw(absolute_file_path)
