from types import NoneType

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.constants import SPOTIFY_API_BASE_URL
from pl_tiny_clients.fetch_spotify_access_token import AccessToken
from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.spotify_api_authorization_headers import (
    spotify_api_authorization_headers,
)


@MockInUnitTests(MockReason.UNINVESTIGATED)
def spotify_set_repeat_track(repeat_track: bool, access_token: AccessToken) -> None:
    """
    Set Spotify repeat mode.

    Args:
        repeat_track (bool): True to repeat the current song, False to repeat the playlist
        access_token (AccessToken): Spotify access token with appropriate scopes.

    """
    # Docs: https://developer.spotify.com/documentation/web-api

    state = "track" if repeat_track else "context"

    requests_wrapper(
        f"{SPOTIFY_API_BASE_URL}/me/player/repeat",
        NoneType,
        method="PUT",
        query_params={"state": state},
        temp_override_for_spotify_204_bug=True,
        headers=spotify_api_authorization_headers(access_token),
    )
