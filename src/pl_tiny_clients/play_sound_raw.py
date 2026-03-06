from pathlib import Path

from pl_tiny_clients.by_platform import by_platform
from pl_tiny_clients.play_sound_raw_on_mac import play_sound_raw_on_mac
from pl_tiny_clients.play_sound_raw_on_ubuntu import play_sound_raw_on_ubuntu


def play_sound_raw(absolute_file_path: Path) -> None:
    # You should probably use `play_sound` instead, which sets the volume first.

    by_platform(
        mac=play_sound_raw_on_mac,
        ubuntu=play_sound_raw_on_ubuntu,
    )(absolute_file_path)
