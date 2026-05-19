from types import NoneType

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.constants import SPOTIFY_API_BASE_URL
from pl_tiny_clients.fetch_spotify_access_token import AccessToken
from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.spotify_api_authorization_headers import (
    spotify_api_authorization_headers,
)


@MockInUnitTests(MockReason.UNINVESTIGATED)
def spotify_remove_tracks(
    playlist_id: str, track_ids: list[str], access_token: AccessToken
) -> None:
    """Per the docs, "A maximum of 100 objects [to be removed] can be sent at once"."""
    # Docs: https://developer.spotify.com/documentation/web-api

    assert len(track_ids) <= 100
    requests_wrapper(
        f"{SPOTIFY_API_BASE_URL}/playlists/{playlist_id}/tracks",
        NoneType,
        method="DELETE",
        body_params={
            "tracks": [{"uri": f"spotify:track:{track_id}"} for track_id in track_ids]
        },
        headers=spotify_api_authorization_headers(access_token),
    )
