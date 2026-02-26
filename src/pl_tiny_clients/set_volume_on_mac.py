from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.execute_shell_command import execute_shell_command


@MockInUnitTests(MockReason.UNINVESTIGATED)
def set_volume_on_mac(volume: int) -> None:
    """
    Set the volume to a value between 0 and 100.

    Only works on a Mac.
    """
    execute_shell_command(f"osascript -e 'set volume output volume {volume}'")
