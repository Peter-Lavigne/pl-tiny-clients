from pl_mocks_and_fakes import fake_for, mock_for
from pl_user_io import task, yes_no

from pl_tiny_clients.constants import PLATFORM_MAC
from pl_tiny_clients.fetch_spotify_access_token import AccessToken
from pl_tiny_clients.notify_on_mac import notify_on_mac
from pl_tiny_clients.settings import get_settings
from pl_tiny_clients.spotify_get_playback_state import spotify_get_playback_state
from pl_tiny_clients.testing.settings_fake import SettingsFake


def ensure_inactive(access_token: AccessToken) -> None:
    if yes_no("Have you played Spotify today?"):
        task("Play Spotify from your desktop, then quit and reopen Spotify.")
    response = spotify_get_playback_state(access_token)
    assert response is None


def assert_notified(text: str, title: str | None = None) -> None:
    assert fake_for(SettingsFake).settings.platform == PLATFORM_MAC
    assert mock_for(get_settings)().platform == PLATFORM_MAC
    if title is None:
        mock_for(notify_on_mac).assert_called_with(text, "Notifier")
    else:
        mock_for(notify_on_mac).assert_called_with(text, title)
