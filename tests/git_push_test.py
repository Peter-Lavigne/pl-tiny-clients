import contextlib
from pathlib import Path

from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.execute_shell_command import execute_shell_command
from pl_tiny_clients.git_commit import git_commit
from pl_tiny_clients.git_push import git_push

pytestmark = PYTEST_INTEGRATION_MARKER


def test_git_push(tmp_path: Path) -> None:
    # Create a repo to act as remote
    remote_path = tmp_path / "remote_repo"
    remote_path.mkdir()
    execute_shell_command(f"git -C {remote_path} init")
    # Allow pushing to the checked-out branch
    execute_shell_command(
        f"git -C {remote_path} config receive.denyCurrentBranch updateInstead"
    )

    # Create a local repo
    repo_path = tmp_path / "local_repo"
    repo_path.mkdir()
    with contextlib.chdir(repo_path):
        execute_shell_command("git init")
        execute_shell_command(f"git remote add origin {remote_path}")

        # Create and commit a file
        (repo_path / "file.txt").write_text("content")
        execute_shell_command("git add file.txt")
        git_commit("Add file.txt")

        # Set upstream and push
        execute_shell_command("git push -u origin HEAD")

        # Verify the push was successful
        log_output = execute_shell_command(f"git -C {remote_path} log --oneline")
        assert "Add file.txt" in log_output


def test_git_push_after_commit(tmp_path: Path) -> None:
    # Create a repo to act as remote
    remote_path = tmp_path / "remote_repo"
    remote_path.mkdir()
    execute_shell_command(f"git -C {remote_path} init")
    # Allow pushing to the checked-out branch
    execute_shell_command(
        f"git -C {remote_path} config receive.denyCurrentBranch updateInstead"
    )

    # Create a local repo with initial commit
    repo_path = tmp_path / "local_repo"
    repo_path.mkdir()
    with contextlib.chdir(repo_path):
        execute_shell_command("git init")
        execute_shell_command(f"git remote add origin {remote_path}")

        (repo_path / "initial.txt").write_text("initial")
        execute_shell_command("git add initial.txt")
        git_commit("Initial commit")

        # Set upstream and push initial commit
        execute_shell_command("git push -u origin HEAD")

        # Make a change and push
        (repo_path / "change.txt").write_text("new")
        execute_shell_command("git add change.txt")
        git_commit("Add change.txt")
        git_push()

        # Verify the change is in remote
        log_output = execute_shell_command(f"git -C {remote_path} log --oneline")
        assert "Add change.txt" in log_output
