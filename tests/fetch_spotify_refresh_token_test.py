from pl_user_io.assert_yes import assert_yes
from pl_user_io.display import display

from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.fetch_spotify_refresh_token import fetch_spotify_refresh_token

pytestmark = PYTEST_INTEGRATION_MARKER


def test_fetch_refresh_token() -> None:
    token = fetch_spotify_refresh_token("")
    assert isinstance(token, str)
    assert_yes(
        "Were you walked through providing information, and possibly approval, needed for a refresh token?"
    )
    display(f"Refresh token: {token}")
