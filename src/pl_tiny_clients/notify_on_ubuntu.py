from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.execute_shell_command import execute_shell_command


@MockInUnitTests(MockReason.UNINVESTIGATED)
def notify_on_ubuntu(text: str, title: str) -> None:
    """Display a notification on Ubuntu."""
    execute_shell_command(f'notify-send -u critical "{title}" "{text}"')
