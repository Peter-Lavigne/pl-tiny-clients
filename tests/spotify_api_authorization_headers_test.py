from pl_tiny_clients.spotify_api_authorization_headers import (
    spotify_api_authorization_headers,
)


def test_returns_authorization_bearer_headers() -> None:
    headers = spotify_api_authorization_headers("fake_access_token")

    assert headers == {"Authorization": "Bearer fake_access_token"}
