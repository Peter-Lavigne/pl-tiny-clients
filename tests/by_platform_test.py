import pytest
from pl_mocks_and_fakes import fake_for

from pl_tiny_clients.by_platform import by_platform
from pl_tiny_clients.constants import PLATFORM_MAC, PLATFORM_UBUNTU
from pl_tiny_clients.testing.settings_fake import SettingsFake


def test_returns_mac_value_on_mac() -> None:
    fake_for(SettingsFake).settings.platform = PLATFORM_MAC

    result = by_platform(mac="MAC_VALUE", ubuntu="UBUNTU_VALUE")

    assert result == "MAC_VALUE"


def test_returns_ubuntu_value_on_ubuntu() -> None:
    fake_for(SettingsFake).settings.platform = PLATFORM_UBUNTU

    result = by_platform(mac="MAC_VALUE", ubuntu="UBUNTU_VALUE")

    assert result == "UBUNTU_VALUE"


def test_raises_error_when_platform_not_set() -> None:
    # Settings default for platform is '' when not set
    fake_for(SettingsFake).settings.platform = ""

    with pytest.raises(ValueError):
        by_platform(mac="MAC_VALUE", ubuntu="UBUNTU_VALUE")


def test_raises_error_on_unsupported_platform() -> None:
    fake_for(SettingsFake).settings.platform = "windows"

    with pytest.raises(ValueError):
        by_platform(mac="MAC_VALUE", ubuntu="UBUNTU_VALUE")
