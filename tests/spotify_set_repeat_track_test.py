from pl_user_io.assert_yes import assert_yes
from pl_user_io.task import task

from pl_tiny_clients.fetch_spotify_access_token import fetch_spotify_access_token
from pl_tiny_clients.spotify_set_repeat_track import spotify_set_repeat_track
from tests.constants import PYTEST_INTEGRATION_MARKER

pytestmark = PYTEST_INTEGRATION_MARKER


def test_set_repeat_track() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    task("Turn repeat off in Spotify.")
    spotify_set_repeat_track(True, access_token)
    assert_yes("Did Spotify set repeat to repeat a single track?")
    spotify_set_repeat_track(False, access_token)
    assert_yes("Did Spotify set repeat to repeat a playlist?")
