from datetime import timedelta

import pytest
from pl_user_io.assert_yes import assert_yes
from pl_user_io.task import task

from pl_tiny_clients.delay import delay
from pl_tiny_clients.fetch_spotify_access_token import fetch_spotify_access_token
from pl_tiny_clients.spotify_get_playback_state import spotify_get_playback_state
from pl_tiny_clients.spotify_skip import spotify_skip
from pl_tiny_clients.testing.assertions import ensure_inactive
from tests.constants import PYTEST_INTEGRATION_MARKER

pytestmark = PYTEST_INTEGRATION_MARKER


def test_skip() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    task("Start playing a song.")
    spotify_skip(access_token)
    assert_yes("Did Spotify skip to the next song?")


def test_skip__delays_updating_currently_playing() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    # This test documents unexpected behavior in the API.
    # See the note in the SpotifyApi.skip function for more information.
    attempts = 20  # Arbitrary number of attempts that consistently exposes the behavior. If this fails, try increasing the number.
    task(f"Start playing a song in a playlist of at least {attempts + 1} songs.")
    for _ in range(attempts):
        start_song = spotify_get_playback_state(access_token)
        assert start_song is not None
        start_song_id = start_song["item"]["id"]

        spotify_skip(access_token)

        maybe_next_song = spotify_get_playback_state(access_token)
        assert maybe_next_song is not None
        maybe_next_song_id = maybe_next_song["item"]["id"]

        if start_song_id == maybe_next_song_id:
            # Behavior exposed
            delay(timedelta(seconds=1))

            actual_next_song = spotify_get_playback_state(access_token)
            assert actual_next_song is not None
            actual_next_song_id = actual_next_song["item"]["id"]

            assert start_song_id != actual_next_song_id
            return
    msg = "Expected currently playing to delay updating after a skip."
    raise AssertionError(msg)


def test_skip__inactive() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    ensure_inactive(access_token)

    with pytest.raises(Exception):
        spotify_skip(access_token)
