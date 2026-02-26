from pl_user_io.assert_yes import assert_yes
from pl_user_io.task import task

from pl_tiny_clients.constants import (
    SPOTIFY_DESKTOP_DEVICE_NAME,
    SPOTIFY_PHONE_DEVICE_NAME,
)
from pl_tiny_clients.fetch_spotify_access_token import (
    fetch_spotify_access_token,
)
from pl_tiny_clients.spotify_get_playback_state import (
    SpotifyArtistResponse,
    SpotifyDeviceResponse,
    SpotifyGetPlaybackStateResponse,
    SpotifyGetPlaybackStateResponseContext,
    SpotifyTrackObject,
    spotify_get_playback_state,
)
from pl_tiny_clients.testing.assertions import ensure_inactive
from pl_tiny_clients.testing.validate_keys import validate_keys
from tests.constants import (
    PYTEST_INTEGRATION_MARKER,
)

pytestmark = PYTEST_INTEGRATION_MARKER


def test_get_playback_state__validate_keys() -> None:
    task("Start playing Spotify.")
    access_token = fetch_spotify_access_token()["access_token"]

    response = spotify_get_playback_state(access_token)

    assert response is not None
    validate_keys(response, SpotifyGetPlaybackStateResponse)
    validate_keys(response["item"], SpotifyTrackObject)
    validate_keys(response["device"], SpotifyDeviceResponse)
    validate_keys(response["context"], SpotifyGetPlaybackStateResponseContext)
    for artist in response["item"]["artists"]:
        validate_keys(artist, SpotifyArtistResponse)


def test_get_playback_state__playing() -> None:
    task("Start playing Spotify.")
    access_token = fetch_spotify_access_token()["access_token"]

    response = spotify_get_playback_state(access_token)

    assert response is not None
    assert_yes(f"Is the currently playing song '{response['item']['name']}'?")


def test_get_playback_state__paused() -> None:
    task("Start playing Spotify, then pause it.")
    access_token = fetch_spotify_access_token()["access_token"]

    response = spotify_get_playback_state(access_token)

    assert response is not None
    assert_yes(f"Is the currently paused song '{response['item']['name']}'?")


def only_test_get_playback_state__computer() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    task("Start playing a song on your iMac.")
    response = spotify_get_playback_state(access_token)
    assert response is not None
    assert response["device"]["name"] == SPOTIFY_DESKTOP_DEVICE_NAME


def test_get_playback_state__phone() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    task("Start playing a song on your phone.")
    response = spotify_get_playback_state(access_token)
    assert response is not None
    assert response["device"]["name"] == SPOTIFY_PHONE_DEVICE_NAME


def test_get_playback_state__no_device() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    ensure_inactive(access_token)

    response = spotify_get_playback_state(access_token)

    assert response is None


def test_get_playback_state__playing_playlist() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    task("Start playing the 'Songs' playlist.")

    response = spotify_get_playback_state(access_token)

    assert response is not None
    assert response["context"] is not None
    assert response["context"]["type"] == "playlist"
    assert (
        response["context"]["href"]
        == "https://api.spotify.com/v1/playlists/5FY8ZBHJpLxWk6Zz9MX3Bw"
    )


def test_get_playback_state__playing_artist() -> None:
    access_token = fetch_spotify_access_token()["access_token"]
    task("Start playing a song from the Neck Deep artist page.")

    response = spotify_get_playback_state(access_token)

    assert response is not None
    assert response["context"] is not None
    assert response["context"]["type"] == "artist"
    assert (
        response["context"]["href"]
        == "https://api.spotify.com/v1/artists/2TM0qnbJH4QPhGMCdPt7fH"
    )
