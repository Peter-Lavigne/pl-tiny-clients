from pl_user_io.assert_yes import assert_yes

from pl_tiny_clients.constants import PLATFORM_MAC, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.notify_on_mac import notify_on_mac
from pl_tiny_clients.settings import get_settings

pytestmark = PYTEST_INTEGRATION_MARKER


def test_sends_notification() -> None:
    assert get_settings().platform == PLATFORM_MAC

    notify_on_mac("This is a test notification.", title="Notifier")

    assert_yes("Did you receive a notification?")
    assert_yes("Is the notification title 'Notifier'?")
    assert_yes("Is the notification message 'This is a test notification.'?")


def test_sends_title() -> None:
    assert get_settings().platform == PLATFORM_MAC

    notify_on_mac("This is a test notification.", title="Test Title")

    assert_yes("Did you receive a notification?")
    assert_yes("Is the notification title 'Test Title'?")
