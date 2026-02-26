from pl_mocks_and_fakes import fake_for, mock_for

from pl_tiny_clients.constants import PLATFORM_MAC, PLATFORM_UBUNTU
from pl_tiny_clients.notify import notify
from pl_tiny_clients.notify_on_mac import notify_on_mac
from pl_tiny_clients.notify_on_ubuntu import notify_on_ubuntu
from pl_tiny_clients.testing.mocks import notify_mock
from pl_tiny_clients.testing.settings_fake import SettingsFake


def test_notifies_on_mac() -> None:
    fake_for(SettingsFake).settings.platform = PLATFORM_MAC

    notify("This is a test notification.", title="Test")

    mock_for(notify_on_mac).assert_called_with("This is a test notification.", "Test")


def test_notifies_on_ubuntu() -> None:
    fake_for(SettingsFake).settings.platform = PLATFORM_UBUNTU

    notify("This is a test notification.", title="Test")

    mock_for(notify_on_ubuntu).assert_called_with(
        "This is a test notification.", "Test"
    )


def test_sets_default_title_to_notifier() -> None:
    notify("This is a test notification.")

    notify_mock().assert_called_with("This is a test notification.", "Notifier")
