import contextlib
from pathlib import Path

from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.execute_shell_command import execute_shell_command
from pl_tiny_clients.git_add_all import git_add_all
from pl_tiny_clients.git_any_uncommitted_changes import git_any_uncommitted_changes
from pl_tiny_clients.git_commit import git_commit

pytestmark = PYTEST_INTEGRATION_MARKER

TEST_FILE = "test.txt"


def _set_up_basic_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir(parents=True)
    (repo / TEST_FILE).write_text("content")
    execute_shell_command(f"git -C {repo} init")
    git_add_all(repo)
    git_commit("Initial commit", repo)
    return repo


def test_git_any_uncommitted_changes__no_changes(tmp_path: Path) -> None:
    repo = _set_up_basic_repo(tmp_path)
    with contextlib.chdir(repo):
        result = git_any_uncommitted_changes()

        assert result is False


def test_git_any_uncommitted_changes__unstaged_changes(tmp_path: Path) -> None:
    repo = _set_up_basic_repo(tmp_path)
    (repo / TEST_FILE).write_text("modified content")
    with contextlib.chdir(repo):
        result = git_any_uncommitted_changes()

        assert result is True


def test_git_any_uncommitted_changes__staged_changes(tmp_path: Path) -> None:
    repo = _set_up_basic_repo(tmp_path)
    (repo / TEST_FILE).write_text("modified content")
    git_add_all(repo)
    with contextlib.chdir(repo):
        result = git_any_uncommitted_changes()

        assert result is True


def test_git_any_uncommitted_changes__untracked_files(tmp_path: Path) -> None:
    repo = _set_up_basic_repo(tmp_path)
    (repo / "untracked.txt").write_text("untracked content")
    with contextlib.chdir(repo):
        result = git_any_uncommitted_changes()

        assert result is True


def test_git_any_uncommitted_changes__repo_parameter__no_changes(
    tmp_path: Path,
) -> None:
    repo = _set_up_basic_repo(tmp_path)

    result = git_any_uncommitted_changes(repo)

    assert result is False


def test_git_any_uncommitted_changes__repo_parameter__changes(tmp_path: Path) -> None:
    repo = _set_up_basic_repo(tmp_path)
    (repo / TEST_FILE).write_text("modified content")

    result = git_any_uncommitted_changes(repo)

    assert result is True
