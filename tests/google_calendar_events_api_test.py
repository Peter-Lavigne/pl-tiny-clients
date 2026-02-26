from datetime import timedelta

from pl_user_io.display import display
from pl_user_io.task_with_url import task_with_url
from pl_user_io.yes_no import yes_no

from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.current_datetime import current_datetime
from pl_tiny_clients.google_calendar_events_api import (
    GoogleCalendarEventBoundary,
    GoogleCalendarEventResponse,
    GoogleCalendarEventsResponse,
    google_calendar_events_api,
)
from pl_tiny_clients.testing.validate_keys import validate_keys

pytestmark = PYTEST_INTEGRATION_MARKER


def test_events() -> None:
    email = "peterklavigne@gmail.com"

    task_with_url(
        f"Create a one-hour event on your {email} calendar starting within an hour of now. Ensure it is the only event.",
        "https://calendar.google.com",
    )

    calendar_settings_url = "https://calendar.google.com/calendar/u/0/r/settings/calendar/cGV0ZXJrbGF2aWduZUBnbWFpbC5jb20"

    task_with_url(f"Change your {email} calendar to be public.", calendar_settings_url)

    events = google_calendar_events_api(
        email,
        (current_datetime() - timedelta(hours=2)),
        (current_datetime() + timedelta(hours=2)),
    )

    validate_keys(events, GoogleCalendarEventsResponse)
    validate_keys(events["items"][0], GoogleCalendarEventResponse)
    validate_keys(events["items"][0]["start"], GoogleCalendarEventBoundary)
    validate_keys(events["items"][0]["end"], GoogleCalendarEventBoundary)

    display(
        f"The returned event starts at {events['items'][0]['start']['dateTime']} and ends at {events['items'][0]['end']['dateTime']}"
    )
    assert yes_no("Does the above match the event you created?")

    task_with_url(f"Change your {email} calendar to be private.", calendar_settings_url)
    task_with_url("Delete the event.", "https://calendar.google.com")
