import re

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.execute_shell_command import execute_shell_command


@MockInUnitTests(MockReason.UNINVESTIGATED)
def get_volume_on_ubuntu() -> int:
    output = execute_shell_command("pactl get-sink-volume @DEFAULT_SINK@")
    # Extract percentage from output like: 0:   50% / 0.50
    match = re.search(r"\s+(\d+)%", output)
    if match:
        return int(match.group(1))
    msg = "Could not determine volume from pactl output."
    raise Exception(msg)
