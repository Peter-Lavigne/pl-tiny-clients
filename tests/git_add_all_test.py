import contextlib
from pathlib import Path

from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.execute_shell_command import execute_shell_command
from pl_tiny_clients.git_add_all import git_add_all

pytestmark = PYTEST_INTEGRATION_MARKER


def test_git_add_all(tmp_path: Path) -> None:
    (tmp_path / "test.txt").write_text("line1\nline2")
    with contextlib.chdir(tmp_path):
        execute_shell_command("git init")

        git_add_all()

        status_output = execute_shell_command("git status")
        assert "test.txt" in status_output
        assert "Changes to be committed" in status_output


def test_git_add_all_multiple_files(tmp_path: Path) -> None:
    (tmp_path / "file1.txt").write_text("content1")
    (tmp_path / "file2.txt").write_text("content2")
    with contextlib.chdir(tmp_path):
        execute_shell_command("git init")

        git_add_all()

        status_output = execute_shell_command("git status")
        assert "file1.txt" in status_output
        assert "file2.txt" in status_output
        assert "Changes to be committed" in status_output


def test_git_add_all__repo_parameter(tmp_path: Path) -> None:
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    (repo_path / "file1.txt").write_text("content1")
    (repo_path / "file2.txt").write_text("content2")
    execute_shell_command(f"git -C {repo_path} init")

    git_add_all(repo_path)

    status_output = execute_shell_command(f"git -C {repo_path} status")
    assert "file1.txt" in status_output
    assert "file2.txt" in status_output
    assert "Changes to be committed" in status_output
