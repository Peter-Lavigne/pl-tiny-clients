import re
from datetime import datetime
from typing import NamedTuple

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.current_datetime import current_datetime
from pl_tiny_clients.execute_shell_command import execute_shell_command


class DisplayPowerEventsOnUbuntuResponse(NamedTuple):
    most_recent_off: datetime
    most_recent_on: datetime


@MockInUnitTests(MockReason.UNINVESTIGATED)
def display_power_events_on_ubuntu() -> DisplayPowerEventsOnUbuntuResponse:
    """
    Return a tuple containing datetimes for the last time the display was turned off and on, respectively.

    Timestamps are in the machine's local timezone.
    """
    output = execute_shell_command(
        "journalctl --since '1 week ago' | grep 'systemd-sleep'"
    )
    lines = output.split("\n")

    most_recent_off = None
    most_recent_on = None

    for line in lines:
        # Extract timestamp from journalctl format: "Dec 08 16:16:14"
        # Pattern: Month Day HH:MM:SS
        match = re.match(r"^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})", line)
        if not match:
            continue

        timestamp_str = match.group(1)
        # Parse with current year (journalctl doesn't include year)
        timestamp = datetime.strptime(
            f"{current_datetime().year} {timestamp_str}", "%Y %b %d %H:%M:%S"
        )

        if "Performing sleep operation 'suspend'" in line:
            most_recent_off = timestamp
        elif "System returned from sleep operation 'suspend'" in line:
            most_recent_on = timestamp

    assert most_recent_off is not None
    assert most_recent_on is not None

    return DisplayPowerEventsOnUbuntuResponse(most_recent_off, most_recent_on)
