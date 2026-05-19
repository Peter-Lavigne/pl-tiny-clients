import pytest
from pl_user_io.assert_yes import assert_yes
from pl_user_io.task import task

from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.fetch_spotify_access_token import fetch_spotify_access_token
from pl_tiny_clients.spotify_get_playback_state import spotify_get_playback_state
from pl_tiny_clients.spotify_remove_tracks import spotify_remove_tracks

pytestmark = PYTEST_INTEGRATION_MARKER


def test_remove_tracks__removes_tracks() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    task("Create a playlist with at least three songs.")
    task("Play one of the songs in the playlist.")
    currently_playing_1 = spotify_get_playback_state(access_token)
    assert currently_playing_1 is not None
    playlist_id = currently_playing_1["context"]["href"].split("/")[-1]
    task("Play another song in the playlist.")
    currently_playing_2 = spotify_get_playback_state(access_token)
    assert currently_playing_2 is not None
    song_1_id = currently_playing_1["item"]["id"]
    song_1_name = currently_playing_1["item"]["name"]
    song_2_id = currently_playing_2["item"]["id"]
    song_2_name = currently_playing_2["item"]["name"]
    assert_yes(
        f"Before deleting anything, just to confirm, are the two songs to delete '{song_1_name}' and '{song_2_name}'?"
    )

    spotify_remove_tracks(playlist_id, [song_1_id, song_2_id], access_token)

    assert_yes("Did Spotify delete the two songs from the current playlist?")

    task("Delete the playlist.")


def test_remove_tracks__prevents_sending_over_100_tracks() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    with pytest.raises(AssertionError):
        spotify_remove_tracks("fake", ["1"] * 101, access_token)
