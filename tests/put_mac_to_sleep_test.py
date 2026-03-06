from pl_user_io.assert_yes import assert_yes

from pl_tiny_clients.constants import PLATFORM_MAC, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.put_mac_to_sleep import put_mac_to_sleep
from pl_tiny_clients.settings import get_settings

pytestmark = PYTEST_INTEGRATION_MARKER


def test_puts_mac_to_sleep() -> None:
    assert get_settings().platform == PLATFORM_MAC, (
        "The test must be run on a Mac machine."
    )

    put_mac_to_sleep()

    assert_yes("Did the test put the Mac to sleep?")
