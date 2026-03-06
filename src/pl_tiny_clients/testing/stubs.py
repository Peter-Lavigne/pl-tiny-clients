from collections.abc import Sequence
from datetime import datetime

from pl_mocks_and_fakes import fake_for, mock_for, stub

from pl_tiny_clients.constants import PLATFORM_MAC, SYSTEM_TIMEZONE
from pl_tiny_clients.display_power_events import DisplayPowerEventsResponse
from pl_tiny_clients.display_power_events_on_mac import (
    DisplayPowerEventsOnMacResponse,
    display_power_events_on_mac,
)
from pl_tiny_clients.fetch_mbta_predictions import (
    MBTAPredictionAttributesResponse,
    MBTAPredictionResponse,
    MBTAPredictionsResponse,
    fetch_mbta_predictions,
)
from pl_tiny_clients.fetch_openweathermap_onecall_api import (
    OpenWeatherMapOneCallResponse,
    OpenWeatherMapWeatherIdResponse,
    OpenWeatherMapWeatherReportResponse,
    fetch_openweathermap_onecall_api,
)
from pl_tiny_clients.fetch_spotify_access_token import SpotifyRefreshResponse
from pl_tiny_clients.get_volume_on_mac import get_volume_on_mac
from pl_tiny_clients.settings import get_settings
from pl_tiny_clients.spotify_get_playback_state import (
    SpotifyGetPlaybackStateResponse,
    spotify_get_playback_state,
)
from pl_tiny_clients.testing.constants import DEFAULT_DATETIME
from pl_tiny_clients.testing.settings_fake import SettingsFake
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


def stub_weather_id_response() -> OpenWeatherMapWeatherIdResponse:
    return {"id": 1}


def stub_weather_report_response() -> OpenWeatherMapWeatherReportResponse:
    return {
        "dt": int(DEFAULT_DATETIME.timestamp()),
        "feels_like": 0.0,
        "weather": [stub_weather_id_response()],
    }


def stub_one_call_response() -> OpenWeatherMapOneCallResponse:
    return {
        "current": stub_weather_report_response(),
        "hourly": [stub_weather_report_response()],
    }


def stub_current_temp(temp: float) -> None:
    stub(fetch_openweathermap_onecall_api)(
        {
            **stub_one_call_response(),
            "current": {**stub_weather_report_response(), "feels_like": temp},
        }
    )


def stub_mbta_prediction_attributes_response() -> MBTAPredictionAttributesResponse:
    return {"departure_time": "2000-01-01T12:00:00-05:00"}


def stub_mbta_prediction_response() -> MBTAPredictionResponse:
    return {"attributes": stub_mbta_prediction_attributes_response()}


def stub_mbta_predictions_response() -> MBTAPredictionsResponse:
    return {"data": [stub_mbta_prediction_response()]}


def stub_fetch_predictions(response: MBTAPredictionsResponse) -> None:
    mock_for(fetch_mbta_predictions).return_value = response


def stub_display_power_events(value: DisplayPowerEventsResponse) -> None:
    """Stubs the `get_volume` function to return the given value."""
    assert fake_for(SettingsFake).settings.platform == PLATFORM_MAC
    assert mock_for(get_settings)().platform == PLATFORM_MAC
    stub(display_power_events_on_mac)(
        DisplayPowerEventsOnMacResponse(value.most_recent_off, value.most_recent_on)
    )


def stub_get_volume(value: int) -> None:
    """Stubs the `get_volume` function to return the given value."""
    assert fake_for(SettingsFake).settings.platform == PLATFORM_MAC
    assert mock_for(get_settings)().platform == PLATFORM_MAC
    stub(get_volume_on_mac)(value)
