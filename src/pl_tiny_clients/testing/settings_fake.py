from pl_mocks_and_fakes import Fake, stub

from pl_tiny_clients.settings import Settings, get_settings


class SettingsFake(Fake):
    def __init__(self) -> None:
        self.settings = Settings(
            spotify_client_secret="",
            spotify_refresh_token="",
            trello_token="",
        )
        self.settings.spotify_client_secret = ""
        self.settings.spotify_refresh_token = ""
        self.settings.trello_token = ""
        stub(get_settings)(self.settings)
