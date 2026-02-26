from pathlib import Path

from pl_mocks_and_fakes import MockInUnitTests, MockReason
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """Settings loaded from env, .env, and secrets dir (local) or AWS Secrets Manager (Lambda)."""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        secrets_dir=Path.home() / ".secrets-files",
    )

    # Secrets (from secrets dir locally, or AWS Secrets Manager when USE_AWS_SECRETS_MANAGER=true)
    spotify_client_secret: str = Field(
        validation_alias="SPOTIFY_CLIENT_SECRET", default=""
    )
    spotify_refresh_token: str = Field(
        validation_alias="SPOTIFY_REFRESH_TOKEN", default=""
    )
    trello_token: str = Field(validation_alias="TRELLO_TOKEN", default="")
    anthropic_api_key: str = Field(validation_alias="ANTHROPIC_API_KEY", default="")
    baseten_api_key: str = Field(validation_alias="BASETEN_API_KEY", default="")
    deepseek_api_key: str = Field(validation_alias="DEEPSEEK_API_KEY", default="")
    openweather_api_key: str = Field(validation_alias="OPENWEATHER_API_KEY", default="")
    mbta_token: str = Field(validation_alias="MBTA_TOKEN", default="")
    google_api_key: str = Field(validation_alias="GOOGLE_API_KEY", default="")


@MockInUnitTests(MockReason.UNMITIGATED_SIDE_EFFECT)
def get_settings() -> Settings:
    """Get settings. Raises exception if required settings are missing or invalid."""
    # Required fields are populated from env/.env at runtime; pyright doesn't model that.
    return Settings()  # pyright: ignore[reportCallIssue]
