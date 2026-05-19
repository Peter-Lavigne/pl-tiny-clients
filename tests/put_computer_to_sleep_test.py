from pl_mocks_and_fakes import fake_for, mock_for

from pl_tiny_clients.constants import PLATFORM_MAC, PLATFORM_UBUNTU
from pl_tiny_clients.put_computer_to_sleep import put_computer_to_sleep
from pl_tiny_clients.put_mac_to_sleep import put_mac_to_sleep
from pl_tiny_clients.put_ubuntu_to_sleep import put_ubuntu_to_sleep
from pl_tiny_clients.testing.settings_fake import SettingsFake


def test_puts_mac_to_sleep() -> None:
    fake_for(SettingsFake).settings.platform = PLATFORM_MAC

    put_computer_to_sleep()

    mock_for(put_mac_to_sleep).assert_called_once()


def test_puts_ubuntu_to_sleep() -> None:
    fake_for(SettingsFake).settings.platform = PLATFORM_UBUNTU

    put_computer_to_sleep()

    mock_for(put_ubuntu_to_sleep).assert_called_once()
