from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.execute_shell_command import execute_shell_command


@MockInUnitTests(MockReason.UNINVESTIGATED)
def get_volume_on_mac() -> int:
    """
    Return the volume as a value between 0 and 100.

    Only works on a Mac.
    """
    return int(
        execute_shell_command("osascript -e 'output volume of (get volume settings)'")
    )
