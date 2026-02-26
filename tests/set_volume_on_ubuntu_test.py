from pl_user_io.assert_yes import assert_yes

from pl_tiny_clients.constants import PLATFORM_UBUNTU, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.set_volume_on_ubuntu import set_volume_on_ubuntu
from pl_tiny_clients.settings import get_settings

pytestmark = PYTEST_INTEGRATION_MARKER


def test_sets_volume() -> None:
    assert get_settings().platform == PLATFORM_UBUNTU

    set_volume_on_ubuntu(0)
    assert_yes("Is the volume muted?")
    set_volume_on_ubuntu(50)
    assert_yes("Is the volume at 50%?")
    set_volume_on_ubuntu(100)
    assert_yes("Is the volume at 100%?")
