from pl_user_io.display import display
from pl_user_io.task_with_url import task_with_url
from pl_user_io.yes_no import yes_no

from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.fetch_mbta_predictions import (
    HARVARD_SQUARE_OUTBOUND_STOP_ID,
    OUTBOUND_FROM_HARVARD_SQUARE_DIRECTION_ID,
    ROUTE_73_ROUTE_ID,
    WOODLEIGH_ROAD_INBOUND_STOP_ID,
    MBTAPredictionAttributesResponse,
    MBTAPredictionResponse,
    MBTAPredictionsResponse,
    fetch_mbta_predictions,
)
from pl_tiny_clients.testing.validate_keys import validate_keys

pytestmark = PYTEST_INTEGRATION_MARKER


def test_fetch_predictions__bus_stop() -> None:
    task_with_url(
        "Check the predictions on the MBTA site.",
        f"https://www.mbta.com/stops/{WOODLEIGH_ROAD_INBOUND_STOP_ID}",
    )

    response = fetch_mbta_predictions(WOODLEIGH_ROAD_INBOUND_STOP_ID)

    validate_keys(response, MBTAPredictionsResponse)
    assert isinstance(response["data"], list)
    assert len(response["data"]) > 0
    validate_keys(response["data"][0], MBTAPredictionResponse)
    validate_keys(response["data"][0]["attributes"], MBTAPredictionAttributesResponse)

    departure_times = ", ".join(
        [d["attributes"]["departure_time"] or "None" for d in response["data"]]
    )
    display(f"Returned departure times: {departure_times}")
    assert yes_no(
        "Do the departure times above match the departure times on the website?"
    )


def test_fetch_predictions__bus_at_station() -> None:
    task_with_url(
        "Check the predictions on the MBTA site.",
        f"https://www.mbta.com/stops/{HARVARD_SQUARE_OUTBOUND_STOP_ID}?route={ROUTE_73_ROUTE_ID}&direction_id={OUTBOUND_FROM_HARVARD_SQUARE_DIRECTION_ID}",
    )

    response = fetch_mbta_predictions(
        HARVARD_SQUARE_OUTBOUND_STOP_ID,
        route_id=ROUTE_73_ROUTE_ID,
        direction_id=OUTBOUND_FROM_HARVARD_SQUARE_DIRECTION_ID,
    )

    validate_keys(response, MBTAPredictionsResponse)
    assert isinstance(response["data"], list)
    assert len(response["data"]) > 0
    validate_keys(response["data"][0], MBTAPredictionResponse)
    validate_keys(response["data"][0]["attributes"], MBTAPredictionAttributesResponse)

    departure_times = ", ".join(
        [d["attributes"]["departure_time"] or "None" for d in response["data"]]
    )
    display(f"Returned departure times: {departure_times}")
    assert yes_no(
        "Do the departure times above match the departure times on the website?"
    )
