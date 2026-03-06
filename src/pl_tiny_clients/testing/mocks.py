from unittest.mock import Mock

from pl_mocks_and_fakes import fake_for, mock_for

from pl_tiny_clients.constants import PLATFORM_MAC
from pl_tiny_clients.display_power_events_on_mac import display_power_events_on_mac
from pl_tiny_clients.get_volume_on_mac import get_volume_on_mac
from pl_tiny_clients.notify_on_mac import notify_on_mac
from pl_tiny_clients.play_sound_raw_on_mac import play_sound_raw_on_mac
from pl_tiny_clients.put_mac_to_sleep import put_mac_to_sleep
from pl_tiny_clients.set_volume_on_mac import set_volume_on_mac
from pl_tiny_clients.settings import get_settings
from pl_tiny_clients.testing.settings_fake import SettingsFake


def notify_mock() -> Mock:
    """Return the default test mock proxying for `notify`."""
    assert fake_for(SettingsFake).settings.platform == PLATFORM_MAC
    assert mock_for(get_settings)().platform == PLATFORM_MAC
    return mock_for(notify_on_mac)


def put_computer_to_sleep_mock() -> Mock:
    """Return the default test mock proxying for `put_computer_to_sleep`."""
    assert fake_for(SettingsFake).settings.platform == PLATFORM_MAC
    assert mock_for(get_settings)().platform == PLATFORM_MAC
    return mock_for(put_mac_to_sleep)


def play_sound_raw_mock() -> Mock:
    """Return the default test mock proxying for `play_sound_raw`."""
    assert fake_for(SettingsFake).settings.platform == PLATFORM_MAC
    assert mock_for(get_settings)().platform == PLATFORM_MAC
    return mock_for(play_sound_raw_on_mac)


def set_volume_mock() -> Mock:
    """Return the default test mock proxying for `set_volume`."""
    assert fake_for(SettingsFake).settings.platform == PLATFORM_MAC
    assert mock_for(get_settings)().platform == PLATFORM_MAC
    return mock_for(set_volume_on_mac)


def get_volume_mock() -> Mock:
    """Return the default test mock proxying for `get_volume`."""
    assert fake_for(SettingsFake).settings.platform == PLATFORM_MAC
    assert mock_for(get_settings)().platform == PLATFORM_MAC
    return mock_for(get_volume_on_mac)


def display_power_events_mock() -> Mock:
    """Return the default test mock proxying for `get_volume`."""
    assert fake_for(SettingsFake).settings.platform == PLATFORM_MAC
    assert mock_for(get_settings)().platform == PLATFORM_MAC
    return mock_for(display_power_events_on_mac)
