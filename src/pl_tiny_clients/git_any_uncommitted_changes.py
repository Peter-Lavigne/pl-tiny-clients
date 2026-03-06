from pathlib import Path

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.execute_shell_command import execute_shell_command


@MockInUnitTests(MockReason.UNINVESTIGATED)
def git_any_uncommitted_changes(repo: Path | None = None) -> bool:
    if repo is None:
        output = execute_shell_command("git status --porcelain")
    else:
        output = execute_shell_command(f"git -C {repo} status --porcelain")
    return len(output.strip()) > 0
