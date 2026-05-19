from types import NoneType

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.execute_shell_command import execute_shell_command


@MockInUnitTests(MockReason.UNINVESTIGATED)
def set_volume_on_ubuntu(volume: int) -> NoneType:
    execute_shell_command(f"pactl set-sink-volume @DEFAULT_SINK@ {volume}%")
