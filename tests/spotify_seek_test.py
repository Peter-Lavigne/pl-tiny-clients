import pytest
from pl_user_io.assert_yes import assert_yes
from pl_user_io.task import task

from pl_tiny_clients.constants import (
    PYTEST_MANUAL_MARKER,
    PYTEST_THIRD_PARTY_API_MARKERS,
)
from pl_tiny_clients.fetch_spotify_access_token import fetch_spotify_access_token
from pl_tiny_clients.spotify_seek import spotify_seek
from pl_tiny_clients.testing.assertions import ensure_inactive

pytestmark = [*PYTEST_THIRD_PARTY_API_MARKERS, PYTEST_MANUAL_MARKER]


def test_seek() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    task("Start playing a song at least one minute long.")
    spotify_seek(0, access_token)
    assert_yes("Did Spotify skip to the start of the song?")
    spotify_seek(60 * 1000, access_token)
    assert_yes("Did Spotify skip to the one minute mark?")


def test_seek__inactive() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    ensure_inactive(access_token)

    with pytest.raises(Exception):
        spotify_seek(0, access_token)
