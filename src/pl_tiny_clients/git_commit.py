from pathlib import Path
from types import NoneType

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.execute_shell_command import execute_shell_command


@MockInUnitTests(MockReason.UNINVESTIGATED)
def git_commit(message: str, repo: Path | None = None) -> NoneType:
    message_with_escaped_quotes = message.replace('"', '\\"')
    if repo is None:
        execute_shell_command(f'git commit -m "{message_with_escaped_quotes}"')
    else:
        execute_shell_command(
            f'git -C {repo} commit -m "{message_with_escaped_quotes}"'
        )
