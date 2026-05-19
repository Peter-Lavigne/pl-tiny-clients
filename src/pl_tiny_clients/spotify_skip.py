from types import NoneType

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.constants import SPOTIFY_API_BASE_URL
from pl_tiny_clients.fetch_spotify_access_token import AccessToken
from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.spotify_api_authorization_headers import (
    spotify_api_authorization_headers,
)


@MockInUnitTests(MockReason.UNINVESTIGATED)
def spotify_skip(access_token: AccessToken) -> None:
    """
    Skip to next song on Spotify.

    Note: There is sometimes a delay between making this request and the time it appears as the
    currently playing song. This delay is not documented. When using, I recommend waiting until
    the song changes before making another request.

    Raises a 404 error if no device is playing. This is not documented.
    The recommended workaround is to play a song on the device first.
    """
    # Docs: https://developer.spotify.com/documentation/web-api

    requests_wrapper(
        f"{SPOTIFY_API_BASE_URL}/me/player/next",
        NoneType,
        method="POST",
        temp_override_for_spotify_204_bug=True,
        headers=spotify_api_authorization_headers(access_token),
    )
