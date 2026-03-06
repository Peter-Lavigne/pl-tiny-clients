from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.execute_shell_command import execute_shell_command


@MockInUnitTests(MockReason.UNINVESTIGATED)
def put_mac_to_sleep() -> None:
    execute_shell_command("osascript -e 'tell application \"Finder\" to sleep'")
