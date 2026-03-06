from datetime import timedelta

from pl_user_io.task import task
from pl_user_io.wait_for_enter import wait_for_enter
from pl_user_io.yes_no import yes_no

from pl_tiny_clients.constants import PLATFORM_MAC, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.current_datetime import current_datetime
from pl_tiny_clients.display_power_events_on_mac import display_power_events_on_mac
from pl_tiny_clients.put_computer_to_sleep import put_computer_to_sleep
from pl_tiny_clients.settings import get_settings

pytestmark = PYTEST_INTEGRATION_MARKER


def test_returns_display_times() -> None:
    assert get_settings().platform == PLATFORM_MAC

    margin_of_error_seconds = 10
    task(
        f"The computer will go to sleep. Wait at least {margin_of_error_seconds * 2} seconds, then turn it back on."
    )
    put_computer_to_sleep()
    off_time = current_datetime()
    wait_for_enter()
    on_time = current_datetime()

    off, on = display_power_events_on_mac()

    margin_of_error = timedelta(seconds=margin_of_error_seconds)
    assert abs(off - off_time) < margin_of_error
    assert abs(on - on_time) < margin_of_error


def test_returns_on_time_for_computer_startup() -> None:
    assert get_settings().platform == PLATFORM_MAC

    assert not yes_no(
        "Has the computer display turned off since the computer was last turned on?"
    )

    _, on = display_power_events_on_mac()

    assert yes_no(f"Did the computer turn on at approximately {on}?")
