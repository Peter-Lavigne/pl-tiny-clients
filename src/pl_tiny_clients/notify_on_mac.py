from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.execute_shell_command import execute_shell_command


@MockInUnitTests(MockReason.UNINVESTIGATED)
def notify_on_mac(text: str, title: str) -> None:
    """Display a macOS notification. See build.py for setup."""
    execute_shell_command(
        f'osascript -e \'tell application "Notifier" to notify("{text}", "{title}")\''
    )
