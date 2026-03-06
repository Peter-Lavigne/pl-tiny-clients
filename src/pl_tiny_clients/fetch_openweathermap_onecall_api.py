from typing import TypedDict

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.settings import get_settings


class OpenWeatherMapOneCallQueryParams(TypedDict):
    lon: float
    lat: float


class OpenWeatherMapWeatherIdResponse(TypedDict):
    id: int


class OpenWeatherMapWeatherReportResponse(TypedDict):
    dt: int
    feels_like: float  # Fahrenheit
    weather: list[OpenWeatherMapWeatherIdResponse]


class OpenWeatherMapOneCallResponse(TypedDict):
    current: OpenWeatherMapWeatherReportResponse
    hourly: list[OpenWeatherMapWeatherReportResponse]


@MockInUnitTests(MockReason.UNINVESTIGATED)
def fetch_openweathermap_onecall_api(
    lon: float,
    lat: float,
) -> OpenWeatherMapOneCallResponse:
    return requests_wrapper(
        "https://api.openweathermap.org/data/3.0/onecall",
        OpenWeatherMapOneCallResponse,
        query_params={
            "lon": lon,
            "lat": lat,
            # API keys are obtained from https://home.openweathermap.org/api_keys
            # They take awhile (from searching around: anywhere from 10 minutes to 2 hours) to start working once created.
            "appid": get_settings().openweather_api_key,
            "units": "imperial",
            "exclude": "minutely,daily,alerts",
        },
    )
