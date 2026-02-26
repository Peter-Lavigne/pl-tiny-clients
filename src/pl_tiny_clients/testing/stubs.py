from collections.abc import Sequence
from datetime import datetime

from pl_mocks_and_fakes import fake_for, mock_for

from pl_tiny_clients.constants import SYSTEM_TIMEZONE
from pl_tiny_clients.fetch_spotify_access_token import SpotifyRefreshResponse
from pl_tiny_clients.spotify_get_playback_state import (
    SpotifyGetPlaybackStateResponse,
    spotify_get_playback_state,
)
from pl_tiny_clients.testing.time_fake import TimeFake


def stub_get_playback_state_responses(
    responses: Sequence[SpotifyGetPlaybackStateResponse | None],
) -> None:
    mock_for(spotify_get_playback_state).side_effect = responses


def stub_get_playback_state_exception(exception: Exception) -> None:
    mock_for(spotify_get_playback_state).side_effect = exception


def stub_spotify_refresh_response() -> SpotifyRefreshResponse:
    return {"access_token": "", "expires_in": 0}


def stub_current_datetime(dt: datetime) -> None:
    dt_without_timezone = dt.replace(tzinfo=SYSTEM_TIMEZONE)
    fake_for(TimeFake).set_current_time(dt_without_timezone.timestamp())
