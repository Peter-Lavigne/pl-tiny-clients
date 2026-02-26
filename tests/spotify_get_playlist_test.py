from pl_user_io.assert_yes import assert_yes
from pl_user_io.str_input import str_input
from pl_user_io.task import task

from pl_tiny_clients.fetch_spotify_access_token import fetch_spotify_access_token
from pl_tiny_clients.spotify_get_playback_state import SpotifyTrackObject
from pl_tiny_clients.spotify_get_playlist import (
    SpotifyGetPlaylistResponse,
    SpotifyGetPlaylistTrackResponse,
    SpotifyGetPlaylistTracksResponse,
    spotify_get_playlist,
)
from pl_tiny_clients.testing.validate_keys import validate_keys
from tests.constants import PYTEST_INTEGRATION_MARKER

pytestmark = PYTEST_INTEGRATION_MARKER


def test_get_playlist() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    task("Create a playlist with two different songs.")
    playlist_id = str_input("What is the playlist id?")

    response = spotify_get_playlist(playlist_id, access_token)

    validate_keys(response, SpotifyGetPlaylistResponse)
    validate_keys(response["tracks"], SpotifyGetPlaylistTracksResponse)
    assert len(response["tracks"]["items"]) == 2
    for track in response["tracks"]["items"]:
        validate_keys(track, SpotifyGetPlaylistTrackResponse)
        validate_keys(track["track"], SpotifyTrackObject)
    assert_yes(
        f'Is the first song named "{response["tracks"]["items"][0]["track"]["name"]}"?'
    )
    assert_yes(
        f'Is the second song named "{response["tracks"]["items"][1]["track"]["name"]}"?'
    )

    task("Delete the playlist.")


def test_get_playlist__handles_pagination() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    # 100 is the default pagination length
    task("Create a playlist with 101 songs.")
    playlist_id = str_input("What is the playlist id?")

    response = spotify_get_playlist(playlist_id, access_token)

    assert len(response["tracks"]["items"]) == 101
    assert_yes(
        f'Is the first song named "{response["tracks"]["items"][0]["track"]["name"]}"?'
    )
    assert_yes(
        f'Is the last song named "{response["tracks"]["items"][-1]["track"]["name"]}"?'
    )
