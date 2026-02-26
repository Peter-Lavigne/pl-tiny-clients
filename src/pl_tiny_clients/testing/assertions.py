from pl_user_io import task, yes_no

from pl_tiny_clients.fetch_spotify_access_token import AccessToken
from pl_tiny_clients.spotify_get_playback_state import spotify_get_playback_state


def ensure_inactive(access_token: AccessToken) -> None:
    if yes_no("Have you played Spotify today?"):
        task("Play Spotify from your desktop, then quit and reopen Spotify.")
    response = spotify_get_playback_state(access_token)
    assert response is None
