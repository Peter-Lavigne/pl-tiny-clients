from pathlib import Path
from unittest.mock import Mock

from pl_tiny_clients.play_sound import play_sound
from pl_tiny_clients.testing.mocks import play_sound_raw_mock, set_volume_mock


def play_sound_mock() -> tuple[Mock, Mock]:
    return (play_sound_raw_mock(), set_volume_mock())


def test_plays_sound() -> None:
    file_name = Path("fake_file.mp3")

    play_sound(file_name, 60)

    play_sound_raw_mock().assert_called_once_with(file_name)


def test_sets_volume() -> None:
    play_sound(Path("fake_file.mp3"), 60)

    set_volume_mock().assert_called_with(60)
