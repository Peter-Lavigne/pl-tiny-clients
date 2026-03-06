from pl_tiny_clients.constants import PLATFORM_UBUNTU, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.get_volume_on_ubuntu import get_volume_on_ubuntu
from pl_tiny_clients.set_volume_on_ubuntu import set_volume_on_ubuntu
from pl_tiny_clients.settings import get_settings

pytestmark = PYTEST_INTEGRATION_MARKER


def test_gets_volume() -> None:
    assert get_settings().platform == PLATFORM_UBUNTU

    set_volume_on_ubuntu(0)
    assert get_volume_on_ubuntu() == 0
    set_volume_on_ubuntu(50)
    assert get_volume_on_ubuntu() == 50
    set_volume_on_ubuntu(100)
    assert get_volume_on_ubuntu() == 100
