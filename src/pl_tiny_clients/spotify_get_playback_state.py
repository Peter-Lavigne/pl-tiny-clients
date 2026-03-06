from types import NoneType
from typing import Literal, TypedDict, cast

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.constants import SPOTIFY_API_BASE_URL
from pl_tiny_clients.fetch_spotify_access_token import AccessToken
from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.spotify_api_authorization_headers import (
    spotify_api_authorization_headers,
)


class SpotifyDeviceResponse(TypedDict):
    name: str


class SpotifyGetPlaybackStateResponseContext(TypedDict):
    type: Literal["playlist", "artist"]
    href: str


class SpotifyArtistResponse(TypedDict):
    id: str
    name: str


# "TrackObject" is a term used in the API. Example:
# https://developer.spotify.com/documentation/web-api/reference/get-information-about-the-users-current-playback
class SpotifyTrackObject(TypedDict):
    id: str
    name: str
    duration_ms: int
    artists: list[SpotifyArtistResponse]
    uri: str


class SpotifyGetPlaybackStateResponse(TypedDict):
    device: SpotifyDeviceResponse
    item: SpotifyTrackObject
    context: SpotifyGetPlaybackStateResponseContext


@MockInUnitTests(MockReason.UNINVESTIGATED)
def spotify_get_playback_state(
    access_token: AccessToken,
) -> SpotifyGetPlaybackStateResponse | NoneType:
    """
    Fetch the current playback state. Returns None if there is no active device.

    This happens if Spotify has not been played in awhile or was recently quit.

    This endpoint is equivalent to the currently-playing endpoint but it
    documents the 204 response code so I use this instead.
    """
    # Docs: https://developer.spotify.com/documentation/web-api

    return cast(
        "SpotifyGetPlaybackStateResponse | NoneType",
        requests_wrapper(
            f"{SPOTIFY_API_BASE_URL}/me/player",
            SpotifyGetPlaybackStateResponse,
            possibly_none_expected=True,
            headers=spotify_api_authorization_headers(access_token),
        ),
    )
