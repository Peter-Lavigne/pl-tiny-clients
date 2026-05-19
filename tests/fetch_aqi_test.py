from pl_user_io.display import display
from pl_user_io.task_with_url import task_with_url
from pl_user_io.yes_no import yes_no

from pl_tiny_clients.constants import BOSTON_LAT, BOSTON_LON, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.fetch_aqi import AQICurrentResponse, AQIResponse, fetch_aqi
from pl_tiny_clients.testing.validate_keys import validate_keys

pytestmark = PYTEST_INTEGRATION_MARKER


def test_fetch_aqi() -> None:
    task_with_url(
        "Check the AQI for Framingham.",
        f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={BOSTON_LAT}&longitude={BOSTON_LON}&current=us_aqi",
    )

    response = fetch_aqi(BOSTON_LAT, BOSTON_LON)

    validate_keys(response, AQIResponse)
    validate_keys(response["current"], AQICurrentResponse)

    display(f"Returned AQI: {response['current']['us_aqi']}")
    assert yes_no("Is the above the correct AQI value?")
