from typing import TypedDict

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.requests_wrapper import requests_wrapper


class AQICurrentResponse(TypedDict):
    us_aqi: int


class AQIResponse(TypedDict):
    current: AQICurrentResponse


@MockInUnitTests(MockReason.UNINVESTIGATED)
def fetch_aqi(latitude: float, longitude: float) -> AQIResponse:
    return requests_wrapper(
        f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&current=us_aqi",
        AQIResponse,
    )
