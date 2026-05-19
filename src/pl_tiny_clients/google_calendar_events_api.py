import urllib.parse
from datetime import datetime
from typing import TypedDict

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.settings import get_settings


class GoogleCalendarEventBoundary(TypedDict):
    dateTime: str


class GoogleCalendarEventResponse(TypedDict):
    start: GoogleCalendarEventBoundary
    end: GoogleCalendarEventBoundary


class GoogleCalendarEventsResponse(TypedDict):
    items: list[GoogleCalendarEventResponse]


@MockInUnitTests(MockReason.UNINVESTIGATED)
def google_calendar_events_api(
    email: str, time_min: datetime, time_max: datetime
) -> GoogleCalendarEventsResponse:
    """
    List events for a publicly-shared Google Calendar.

    Docs: https://developers.google.com/calendar/api/v3/reference/events/list
    """
    url_safe_email = urllib.parse.quote(email)
    return requests_wrapper(
        f"https://www.googleapis.com/calendar/v3/calendars/{url_safe_email}/events",
        GoogleCalendarEventsResponse,
        query_params={
            # GOOGLE_API_KEY is obtained from https://console.cloud.google.com/apis/credentials
            # My key is located in a project named "scripts" and is named "bin-XXXXX" where XXXXX is a random string.
            # The key should be restricted to the Google Calendar API
            "key": get_settings().google_api_key,
            # From docs: "Must be an RFC3339 timestamp with mandatory time zone offset"
            "timeMin": time_min.astimezone().isoformat(),
            "timeMax": time_max.astimezone().isoformat(),
        },
    )
