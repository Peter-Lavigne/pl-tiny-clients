from pathlib import Path

from pl_user_io.assert_yes import assert_yes

from pl_tiny_clients.constants import PLATFORM_MAC, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.play_sound_raw_on_mac import play_sound_raw_on_mac
from pl_tiny_clients.set_volume import set_volume
from pl_tiny_clients.settings import get_settings

pytestmark = PYTEST_INTEGRATION_MARKER


def test_plays_sound() -> None:
    assert get_settings().platform == PLATFORM_MAC

    set_volume(20)

    play_sound_raw_on_mac(Path(get_settings().play_sound_test_wav_absolute_path))

    assert_yes("Did a sound play?")
