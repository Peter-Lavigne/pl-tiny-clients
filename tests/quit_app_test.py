from pl_user_io.assert_yes import assert_yes
from pl_user_io.task import task

from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.quit_app import quit_app

pytestmark = PYTEST_INTEGRATION_MARKER


def test_quits_app() -> None:
    task("Ensure VS Code is open.")

    quit_app("/Applications/Visual Studio Code.app")

    assert_yes("Did VS Code quit?")


def test_doesnt_error_for_closed_apps() -> None:
    task("Enture VS Code is closed.")

    # No error is thrown
    quit_app("/Applications/Visual Studio Code.app")
