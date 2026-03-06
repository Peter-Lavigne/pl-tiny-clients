from pprint import pprint

from pl_user_io.assert_yes import assert_yes
from pl_user_io.display import display

from pl_tiny_clients.constants import BOSTON_LAT, BOSTON_LON, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.fetch_openweathermap_onecall_api import (
    OpenWeatherMapOneCallResponse,
    OpenWeatherMapWeatherIdResponse,
    OpenWeatherMapWeatherReportResponse,
    fetch_openweathermap_onecall_api,
)
from pl_tiny_clients.testing.validate_keys import validate_keys

pytestmark = PYTEST_INTEGRATION_MARKER


def test_fetch_onecall() -> None:
    response = fetch_openweathermap_onecall_api(BOSTON_LON, BOSTON_LAT)

    validate_keys(response, OpenWeatherMapOneCallResponse)
    validate_keys(response["current"], OpenWeatherMapWeatherReportResponse)
    validate_keys(response["hourly"][0], OpenWeatherMapWeatherReportResponse)
    validate_keys(response["current"]["weather"][0], OpenWeatherMapWeatherIdResponse)
    validate_keys(response["hourly"][0]["weather"][0], OpenWeatherMapWeatherIdResponse)

    assert len(response["hourly"]) == 48, "Expected 48 hours of forecast data"

    display("Current weather in Boston:")
    pprint(response["current"])
    assert_yes("Does the response seem correct?")
    display("Forecast for a few hours from now:")
    pprint(response["hourly"][3])
    assert_yes("Does the response seem correct?")
    display("Test passed.")
