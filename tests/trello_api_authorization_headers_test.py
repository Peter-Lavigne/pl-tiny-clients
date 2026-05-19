from pl_mocks_and_fakes import fake_for

from pl_tiny_clients.testing.settings_fake import SettingsFake
from pl_tiny_clients.trello_api_authorization_headers import (
    trello_api_authorization_headers,
)


def test_returns_authorization_headers() -> None:
    fake_for(SettingsFake).settings.trello_api_key = "fake_api_key"
    fake_for(SettingsFake).settings.trello_token = "12345"

    headers = trello_api_authorization_headers()

    assert headers == {
        "Authorization": 'OAuth oauth_consumer_key="fake_api_key", oauth_token="12345"'
    }
