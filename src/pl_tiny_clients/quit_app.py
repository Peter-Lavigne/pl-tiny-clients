from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.execute_shell_command import execute_shell_command


@MockInUnitTests(MockReason.UNINVESTIGATED)
def quit_app(app: str) -> None:
    execute_shell_command(f"osascript -e 'quit app \"{app}\"'")
