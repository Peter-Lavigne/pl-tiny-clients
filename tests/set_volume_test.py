from pl_mocks_and_fakes import fake_for, mock_for

from pl_tiny_clients.constants import PLATFORM_MAC, PLATFORM_UBUNTU
from pl_tiny_clients.set_volume import set_volume
from pl_tiny_clients.set_volume_on_mac import set_volume_on_mac
from pl_tiny_clients.set_volume_on_ubuntu import set_volume_on_ubuntu
from pl_tiny_clients.testing.settings_fake import SettingsFake


def test_sets_volume_on_mac() -> None:
    fake_for(SettingsFake).settings.platform = PLATFORM_MAC

    set_volume(30)

    mock_for(set_volume_on_mac).assert_called_once_with(30)


def test_sets_volume_on_ubuntu() -> None:
    fake_for(SettingsFake).settings.platform = PLATFORM_UBUNTU

    set_volume(70)

    mock_for(set_volume_on_ubuntu).assert_called_once_with(70)
