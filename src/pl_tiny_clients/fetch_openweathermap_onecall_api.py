from typing import TypedDict

import httpx
from pl_mocks_and_fakes import MockInUnitTests, THIRD_PARTY_API_MOCK_REASONS

from pl_tiny_clients.settings import get_settings

# Todos:
# - Show less information to users when manual testing, or split into multiple tests
# - Use pydantic for data validation


class OpenWeatherMapWeatherIdResponse(TypedDict):
    id: int  # Weather condition ID, from https://openweathermap.org/weather-conditions


class OpenWeatherMapWeatherReportResponse(TypedDict):
    dt: int  # Unix timestamp
    feels_like: float  # Fahrenheit
    uvi: float
    weather: list[OpenWeatherMapWeatherIdResponse]


class OpenWeatherMapOneCallResponse(TypedDict):
    current: OpenWeatherMapWeatherReportResponse
    hourly: list[OpenWeatherMapWeatherReportResponse]


@MockInUnitTests(*THIRD_PARTY_API_MOCK_REASONS)
def fetch_openweathermap_onecall_api(
    lon: float,
    lat: float,
) -> OpenWeatherMapOneCallResponse:
    response = httpx.get(
        "https://api.openweathermap.org/data/3.0/onecall",
        params={
            "lon": lon,
            "lat": lat,
            # API keys are obtained from https://home.openweathermap.org/api_keys
            # They take awhile (from searching around: anywhere from 10 minutes to 2 hours) to start working once created.
            "appid": get_settings().openweather_api_key,
            "units": "imperial",
            "exclude": "minutely,daily,alerts",
        },
    )

    response.raise_for_status()
    return response.json()
