import contextlib
from pathlib import Path

from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.execute_shell_command import execute_shell_command
from pl_tiny_clients.git_commit import git_commit

pytestmark = PYTEST_INTEGRATION_MARKER


def test_git_commit(tmp_path: Path) -> None:
    directory = tmp_path / "git-test"
    directory.mkdir()
    (directory / "test.txt").write_text("line1\nline2")
    with contextlib.chdir(directory):
        execute_shell_command("git init")
        execute_shell_command("git add test.txt")

        git_commit("Add test.txt")

        log_output = execute_shell_command("git log --oneline")
        assert "Add test.txt" in log_output


def test_commits_messages_with_quotes(tmp_path: Path) -> None:
    directory = tmp_path / "git-test-quotes"
    directory.mkdir()
    (directory / "test.txt").write_text("line1\nline2")
    with contextlib.chdir(directory):
        execute_shell_command("git init")
        execute_shell_command("git add test.txt")

        git_commit('Fix "special" issue')

        log_output = execute_shell_command("git log --oneline")
        assert 'Fix "special" issue' in log_output


def test_git_commit__repo_parameter(tmp_path: Path) -> None:
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    (repo_path / "file1.txt").write_text("content1")
    execute_shell_command(f"git -C {repo_path} init")
    execute_shell_command(f"git -C {repo_path} add file1.txt")

    git_commit("Add file1.txt", repo_path)

    log_output = execute_shell_command(f"git -C {repo_path} log --oneline")
    assert "Add file1.txt" in log_output


def test_git_commit__repo_parameter_with_quotes(tmp_path: Path) -> None:
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    (repo_path / "file1.txt").write_text("content1")
    execute_shell_command(f"git -C {repo_path} init")
    execute_shell_command(f"git -C {repo_path} add file1.txt")

    git_commit('Fix "critical" bug', repo_path)

    log_output = execute_shell_command(f"git -C {repo_path} log --oneline")
    assert 'Fix "critical" bug' in log_output
