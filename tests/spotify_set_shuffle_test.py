import pytest
from pl_user_io.assert_yes import assert_yes
from pl_user_io.task import task

from pl_tiny_clients.fetch_spotify_access_token import fetch_spotify_access_token
from pl_tiny_clients.spotify_set_shuffle import spotify_set_shuffle
from pl_tiny_clients.testing.assertions import ensure_inactive
from tests.constants import PYTEST_INTEGRATION_MARKER

pytestmark = PYTEST_INTEGRATION_MARKER


def test_set_shuffle() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    task("Turn shuffle off in Spotify.")
    spotify_set_shuffle(True, access_token)
    assert_yes("Did Spotify turn on shuffle?")
    spotify_set_shuffle(False, access_token)
    assert_yes("Did Spotify turn off shuffle?")


def test_set_shuffle__inactive() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    ensure_inactive(access_token)

    with pytest.raises(Exception):
        spotify_set_shuffle(True, access_token)
