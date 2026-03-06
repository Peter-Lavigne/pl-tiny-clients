from pl_tiny_clients.constants import PLATFORM_MAC, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.get_volume_on_mac import get_volume_on_mac
from pl_tiny_clients.set_volume_on_mac import set_volume_on_mac
from pl_tiny_clients.settings import get_settings

pytestmark = PYTEST_INTEGRATION_MARKER


def test_gets_volume() -> None:
    assert get_settings().platform == PLATFORM_MAC

    set_volume_on_mac(0)
    assert get_volume_on_mac() == 0
    set_volume_on_mac(50)
    assert get_volume_on_mac() == 50
    set_volume_on_mac(100)
    assert get_volume_on_mac() == 100
