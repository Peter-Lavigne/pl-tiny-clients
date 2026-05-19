from pathlib import Path
from types import NoneType

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.execute_shell_command import execute_shell_command


@MockInUnitTests(MockReason.UNINVESTIGATED)
def git_add_all(repo: Path | None = None) -> NoneType:
    if repo is None:
        execute_shell_command("git add -A")
    else:
        execute_shell_command(f"git -C {repo} add -A")
