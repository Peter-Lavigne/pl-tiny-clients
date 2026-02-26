from datetime import timedelta
from pathlib import Path

from pl_user_io.assert_yes import assert_yes
from pl_user_io.display import display
from pl_user_io.task import task

from pl_tiny_clients.constants import PLATFORM_UBUNTU, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.delay import delay
from pl_tiny_clients.play_sound_raw_on_ubuntu import play_sound_raw_on_ubuntu
from pl_tiny_clients.set_volume import set_volume
from pl_tiny_clients.settings import get_settings

pytestmark = PYTEST_INTEGRATION_MARKER


def test_plays_sound() -> None:
    assert get_settings().platform == PLATFORM_UBUNTU

    set_volume(100)

    play_sound_raw_on_ubuntu(Path(get_settings().play_sound_test_wav_absolute_path))

    assert_yes("Did a sound play?")


def test_plays_sound_at_correct_volume() -> None:
    # This test will only fail consistently when single-threaded
    # Pulse will suspend the sink after a few seconds of silence, causing the next sound to be inaudible. This test demonstrates that we've disabled that behavior.
    # I fixed this by playing a short silence sound before every sound, but there were still edge cases at the 5-second mark (see below), so it's now fixed by disabling sink suspension entirely.

    display("Waiting 6 seconds to allow Pulse to suspend the sink...")
    delay(timedelta(seconds=6))
    display("Continuing test...")
    set_volume(100)

    play_sound_raw_on_ubuntu(Path(get_settings().play_sound_test_wav_absolute_path))
    # Done a second time for comparison
    play_sound_raw_on_ubuntu(Path(get_settings().play_sound_test_wav_absolute_path))

    assert_yes("Did the sound play twice at full volume?")


def test_plays_sound_after_5_second_delay_from_previous_sound() -> None:
    # This was a bug noticed on 2026-01-05.
    # This does not fail for any of the following delays:
    # - 4 seconds
    # - 4.5 seconds
    # - 5.5 seconds
    # - 6 seconds
    # This is because 5 seconds is exactly when Pulse suspends the sink due to inactivity. There must be issues playing a sound immediately while entering or resuming from suspension.
    # See test_plays_sound_at_correct_volume for more details.

    task(
        "Excluding the 'task' sound, you should hear a sound played 5 times, each 5 seconds apart."
    )

    for _ in range(5):
        delay(timedelta(seconds=5))
        display("Playing sound...")
        play_sound_raw_on_ubuntu(Path(get_settings().play_sound_test_wav_absolute_path))

    assert_yes("Did you hear the sound played 5 times, each 5 seconds apart?")
