from pl_mocks_and_fakes import fake_for

from pl_tiny_clients.constants import TRELLO_API_KEY
from pl_tiny_clients.testing.settings_fake import SettingsFake
from pl_tiny_clients.trello_api_authorization_headers import (
    trello_api_authorization_headers,
)


def test_returns_authorization_headers() -> None:
    fake_for(SettingsFake).settings.trello_token = "12345"

    headers = trello_api_authorization_headers()

    assert headers == {
        "Authorization": f'OAuth oauth_consumer_key="{TRELLO_API_KEY}", oauth_token="12345"'
    }
