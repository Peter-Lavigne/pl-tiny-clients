from pathlib import Path

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.execute_shell_command import execute_shell_command


@MockInUnitTests(MockReason.UNINVESTIGATED)
def play_sound_raw_on_mac(absolute_file_path: Path) -> None:
    # You should probably use `play_sound_raw` instead, which is platform-agnostic.
    execute_shell_command(f"afplay {absolute_file_path}")
