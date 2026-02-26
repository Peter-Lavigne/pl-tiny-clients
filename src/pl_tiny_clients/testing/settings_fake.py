from pl_mocks_and_fakes import Fake, stub

from pl_tiny_clients.settings import Settings, get_settings


class SettingsFake(Fake):
    def __init__(self) -> None:
        self.settings = Settings(
            spotify_client_secret="",
            spotify_refresh_token="",
            trello_token="",
            anthropic_api_key="",
            baseten_api_key="",
            deepseek_api_key="",
            openweather_api_key="",
            mbta_token="",
        )
        self.settings.spotify_client_secret = ""
        self.settings.spotify_refresh_token = ""
        self.settings.trello_token = ""
        self.settings.anthropic_api_key = ""
        self.settings.baseten_api_key = ""
        self.settings.deepseek_api_key = ""
        self.settings.openweather_api_key = ""
        self.settings.mbta_token = ""
        stub(get_settings)(self.settings)
