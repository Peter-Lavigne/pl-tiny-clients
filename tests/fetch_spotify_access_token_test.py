from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.fetch_spotify_access_token import (
    SpotifyRefreshResponse,
    fetch_spotify_access_token,
)
from pl_tiny_clients.spotify_set_shuffle import spotify_set_shuffle
from pl_tiny_clients.testing.validate_keys import validate_keys

pytestmark = PYTEST_INTEGRATION_MARKER


def test_fetch_access_token() -> None:
    response = fetch_spotify_access_token()
    validate_keys(response, SpotifyRefreshResponse)

    # Ensure no errors are raised
    spotify_set_shuffle(True, response["access_token"])
