from pl_user_io.assert_yes import assert_yes
from pl_user_io.task import task

from pl_tiny_clients.constants import PLATFORM_UBUNTU, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.notify_on_ubuntu import notify_on_ubuntu
from pl_tiny_clients.settings import get_settings

pytestmark = PYTEST_INTEGRATION_MARKER


def test_sends_notification() -> None:
    assert get_settings().platform == PLATFORM_UBUNTU

    notify_on_ubuntu("This is a test notification.", title="Notifier")

    assert_yes("Did you receive a notification?")
    assert_yes("Is the notification title 'Notifier'?")
    assert_yes("Is the notification message 'This is a test notification.'?")


def test_waits_until_user_clicks() -> None:
    assert get_settings().platform == PLATFORM_UBUNTU
    task("When the notification appears, wait 10 seconds before clicking it.")

    notify_on_ubuntu(
        "This is a test notification that requires clicking.", title="Notifier"
    )

    assert_yes("Did the notification stay until you clicked it?")
