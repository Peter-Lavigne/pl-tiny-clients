from typing import TypedDict

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.constants import SPOTIFY_CLIENT_ID
from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.settings import get_settings

AccessToken = str


class SpotifyRefreshResponse(TypedDict):
    access_token: AccessToken
    expires_in: int


@MockInUnitTests(MockReason.UNINVESTIGATED)
def fetch_spotify_access_token() -> SpotifyRefreshResponse:
    # https://developer.spotify.com/documentation/web-api/tutorials/code-flow

    # Step 3: Request a refreshed Access Token
    return requests_wrapper(
        "https://accounts.spotify.com/api/token",
        SpotifyRefreshResponse,
        method="POST",
        body_params={
            "grant_type": "refresh_token",
            # Refresh tokens are manually generated and placed in .env.
            # The tokens apparently last forever: https://github.com/spotify/web-api/issues/911#issuecomment-581104335
            "refresh_token": get_settings().spotify_refresh_token,
        },
        json=False,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        auth=(SPOTIFY_CLIENT_ID, get_settings().spotify_client_secret),
    )
