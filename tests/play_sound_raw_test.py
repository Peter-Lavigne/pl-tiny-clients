from pathlib import Path

from pl_mocks_and_fakes import fake_for, mock_for

from pl_tiny_clients.constants import PLATFORM_MAC, PLATFORM_UBUNTU
from pl_tiny_clients.play_sound_raw import play_sound_raw
from pl_tiny_clients.play_sound_raw_on_mac import play_sound_raw_on_mac
from pl_tiny_clients.play_sound_raw_on_ubuntu import play_sound_raw_on_ubuntu
from pl_tiny_clients.testing.settings_fake import SettingsFake


def test_plays_sound_on_mac() -> None:
    fake_for(SettingsFake).settings.platform = PLATFORM_MAC

    play_sound_raw(Path("fake_file.mp3"))

    mock_for(play_sound_raw_on_mac).assert_called_once_with(Path("fake_file.mp3"))


def test_plays_sound_on_ubuntu() -> None:
    fake_for(SettingsFake).settings.platform = PLATFORM_UBUNTU

    play_sound_raw(Path("fake_file_2.mp3"))

    mock_for(play_sound_raw_on_ubuntu).assert_called_once_with(Path("fake_file_2.mp3"))
