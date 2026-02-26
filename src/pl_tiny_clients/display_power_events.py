from datetime import datetime
from typing import NamedTuple

from pl_tiny_clients.by_platform import by_platform
from pl_tiny_clients.current_datetime import current_datetime
from pl_tiny_clients.display_power_events_on_mac import (
    DisplayPowerEventsOnMacResponse,
    display_power_events_on_mac,
)


class DisplayPowerEventsResponse(NamedTuple):
    most_recent_off: datetime
    most_recent_on: datetime


def display_power_events() -> (
    DisplayPowerEventsOnMacResponse | DisplayPowerEventsResponse
):
    return by_platform(
        mac=display_power_events_on_mac,
        ubuntu=lambda: DisplayPowerEventsResponse(
            current_datetime(), current_datetime()
        ),
    )()
