from typing import TypedDict

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.constants import SPOTIFY_API_BASE_URL
from pl_tiny_clients.fetch_spotify_access_token import AccessToken
from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.spotify_api_authorization_headers import (
    spotify_api_authorization_headers,
)
from pl_tiny_clients.spotify_get_playback_state import SpotifyTrackObject


class SpotifyGetPlaylistTrackResponse(TypedDict):
    track: SpotifyTrackObject


class SpotifyGetPlaylistTracksResponse(TypedDict):
    next: str | None
    items: list[SpotifyGetPlaylistTrackResponse]


class SpotifyGetPlaylistResponse(TypedDict):
    tracks: SpotifyGetPlaylistTracksResponse


@MockInUnitTests(MockReason.UNINVESTIGATED)
def spotify_get_playlist(
    playlist_id: str, access_token: AccessToken
) -> SpotifyGetPlaylistResponse:
    response = requests_wrapper(
        f"{SPOTIFY_API_BASE_URL}/playlists/{playlist_id}",
        SpotifyGetPlaylistResponse,
        headers=spotify_api_authorization_headers(access_token),
    )

    # Docs: https://developer.spotify.com/documentation/web-api

    next_page_url = response["tracks"]["next"]
    while next_page_url is not None:
        next_page = requests_wrapper(
            next_page_url,
            SpotifyGetPlaylistTracksResponse,
            headers=spotify_api_authorization_headers(access_token),
        )
        response["tracks"]["items"].extend(next_page["items"])
        next_page_url = next_page["next"]

    return response
