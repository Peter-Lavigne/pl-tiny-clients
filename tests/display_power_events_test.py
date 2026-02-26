from pl_mocks_and_fakes import fake_for, mock_for

from pl_tiny_clients.constants import PLATFORM_MAC, PLATFORM_UBUNTU
from pl_tiny_clients.display_power_events import (
    display_power_events,
)
from pl_tiny_clients.display_power_events_on_mac import (
    display_power_events_on_mac,
)
from pl_tiny_clients.testing.settings_fake import SettingsFake


def test_display_power_events_on_mac() -> None:
    fake_for(SettingsFake).settings.platform = PLATFORM_MAC

    display_power_events()

    mock_for(display_power_events_on_mac).assert_called_once()


def test_get_display_power_events_on_ubuntu() -> None:
    fake_for(SettingsFake).settings.platform = PLATFORM_UBUNTU

    display_power_events()

    # No mock to assert; just ensure no exceptions are raised
