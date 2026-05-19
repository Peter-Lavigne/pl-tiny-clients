from typing import TypedDict

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.settings import get_settings

# https://www.mbta.com/stops/2113
WOODLEIGH_ROAD_INBOUND_STOP_ID = "2113"

# https://www.mbta.com/stops/place-harsq?route=73&direction_id=0
HARVARD_SQUARE_OUTBOUND_STOP_ID = "place-harsq"
ROUTE_73_ROUTE_ID = "73"
ROUTE_71_ROUTE_ID = "71"
ROUTE_75_ROUTE_ID = "75"
OUTBOUND_FROM_HARVARD_SQUARE_DIRECTION_ID = "0"


class MBTAPredictionAttributesResponse(TypedDict):
    # arrival_time is None for Harvard Square outbound buses. I'm guessing it's because that's the first stop.
    departure_time: str | None  # "2023-12-29T12:42:01-05:00"


class MBTAPredictionResponse(TypedDict):
    attributes: MBTAPredictionAttributesResponse


class MBTAPredictionsResponse(TypedDict):
    data: list[MBTAPredictionResponse]


@MockInUnitTests(MockReason.UNINVESTIGATED)
def fetch_mbta_predictions(
    stop_id: str, route_id: str | None = None, direction_id: str | None = None
) -> MBTAPredictionsResponse:
    """
    Fetch MBTA predictions for a stop. Note that this API can be very inaccurate.

    For example, I have seen the next predicted bus time decrease by five minutes
    across two calls ten seconds apart.

    Worth noting for future development: There are "arrival_uncertainty" and
    "departure_uncertainty" fields that I could look into.
    """
    # API keys can be obtained from https://api-v3.mbta.com/portal
    api_key = get_settings().mbta_token

    query_params = {"filter[stop]": stop_id}
    if route_id is not None:
        query_params["filter[route]"] = route_id
    if direction_id is not None:
        query_params["filter[direction_id]"] = direction_id

    return requests_wrapper(
        "https://api-v3.mbta.com/predictions",
        MBTAPredictionsResponse,
        query_params=query_params,
        headers={"X-API-Key": api_key},
    )
