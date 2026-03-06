from pl_mocks_and_fakes import fake_for, mock_for

from pl_tiny_clients.constants import PLATFORM_MAC, PLATFORM_UBUNTU
from pl_tiny_clients.get_volume import get_volume
from pl_tiny_clients.get_volume_on_mac import get_volume_on_mac
from pl_tiny_clients.get_volume_on_ubuntu import get_volume_on_ubuntu
from pl_tiny_clients.testing.settings_fake import SettingsFake


def test_gets_volume_on_mac() -> None:
    fake_for(SettingsFake).settings.platform = PLATFORM_MAC

    get_volume()

    mock_for(get_volume_on_mac).assert_called_once()


def test_gets_volume_on_ubuntu() -> None:
    fake_for(SettingsFake).settings.platform = PLATFORM_UBUNTU

    get_volume()

    mock_for(get_volume_on_ubuntu).assert_called_once()
