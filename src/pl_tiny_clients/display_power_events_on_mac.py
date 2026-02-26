import re
from datetime import datetime
from typing import NamedTuple

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.execute_shell_command import execute_shell_command

type Off = datetime
type On = datetime


class DisplayPowerEventsOnMacResponse(NamedTuple):
    most_recent_off: datetime
    most_recent_on: datetime


@MockInUnitTests(MockReason.UNINVESTIGATED)
def display_power_events_on_mac() -> DisplayPowerEventsOnMacResponse:
    """
    Return a tuple containing datetimes for the last time the display was turned off and on, respectively.

    Timestamps are in the machine's local timezone.
    """
    # `pmset -g log` appears to return the last week of logs, so I expect display logs to always be present.
    output = execute_shell_command("pmset -g log")
    lines = output.split("\n")

    def extract_log(line: str) -> tuple[datetime, str, str] | None:
        """
        Return (timestamp, event, message) or None if the line is not a log line.

        This function is imperfect as a small number of log messages contain newlines.
        However, it is good enough for my use case of extracting display logs.
        """
        regex = r"^(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d) [-+]\d\d\d\d ([^\t]+)\t(.+)"
        match = re.match(regex, line)
        if match:
            groups = match.groups()
            timestamp = datetime.strptime(groups[0], "%Y-%m-%d %H:%M:%S")
            event = groups[1].strip()
            message = groups[2].strip()
            return timestamp, event, message
        return None

    most_recent_off = None
    most_recent_on = None

    for line in lines:
        log = extract_log(line)
        if log is None:
            continue
        timestamp, event, message = log
        if event == "Notification":
            if message == "Display is turned off":
                most_recent_off = timestamp
            if message == "Display is turned on":
                most_recent_on = timestamp
        if event == "Start":
            most_recent_on = timestamp

    assert most_recent_off is not None
    assert most_recent_on is not None

    return DisplayPowerEventsOnMacResponse(most_recent_off, most_recent_on)
