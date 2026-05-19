from pl_user_io.assert_yes import assert_yes

from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.open_app import open_app

pytestmark = PYTEST_INTEGRATION_MARKER


def test_opens_vscode() -> None:
    assert_yes("Are you running this test in a terminal window?")
    open_app("/Applications/Visual Studio Code.app")
    assert_yes("Did VS Code open?")


def test_opens_gimp() -> None:
    open_app("/Applications/GIMP-2.10.app")
    assert_yes("Did GIMP open?")


def test_opens_automator() -> None:
    open_app("/System/Applications/Automator.app")
    assert_yes("Did Automator open?")
