import urllib.parse

import requests
from pl_mocks_and_fakes import MockInUnitTests, MockReason
from pl_user_io.str_input import str_input
from pl_user_io.task_with_url import task_with_url

from pl_tiny_clients.constants import SPOTIFY_CLIENT_ID
from pl_tiny_clients.fetch_spotify_access_token import SpotifyRefreshResponse
from pl_tiny_clients.random_str import random_str
from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.settings import get_settings

# API keys are obtained from an app at https://developer.spotify.com/dashboard


class SpotifyTokenResponse(SpotifyRefreshResponse):
    refresh_token: str


@MockInUnitTests(MockReason.UNINVESTIGATED)
def fetch_spotify_refresh_token(scopes: str) -> str:
    # https://developer.spotify.com/documentation/web-api/tutorials/code-flow

    # Step 1: Fetch the authorization code
    state = random_str(40)
    # This value is arbitrary since I don't spin up a server. It must match the redirect URI
    # in the Spotify application settings.
    redirect_uri = "http://127.0.0.1:3000/bin"
    auth_url = (
        requests.Request(
            "GET",
            "https://accounts.spotify.com/authorize",
            params={
                "response_type": "code",
                "client_id": SPOTIFY_CLIENT_ID,
                "redirect_uri": redirect_uri,
                "scope": scopes,
                "state": state,
            },
        )
        .prepare()
        .url
    )
    assert auth_url is not None
    task_with_url("Copy the redirected URL.", auth_url)
    redirected_url = str_input("Paste it here:")
    params = urllib.parse.parse_qs(urllib.parse.urlparse(redirected_url).query)
    assert state == params["state"][0], "OAuth error: state mismatch"
    code = params["code"][0]

    # Step 2: Exchange the authorization code for access and refresh tokens
    response = requests_wrapper(
        "https://accounts.spotify.com/api/token",
        SpotifyTokenResponse,
        method="POST",
        body_params={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        },
        json=False,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        auth=(SPOTIFY_CLIENT_ID, get_settings().spotify_client_secret),
    )
    return response["refresh_token"]
