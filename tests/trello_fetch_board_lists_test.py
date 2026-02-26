from pl_user_io.assert_yes import assert_yes
from pl_user_io.display import display

from pl_tiny_clients.constants import PLANNING_BOARD_ID, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.testing.validate_keys import validate_keys
from pl_tiny_clients.trello_fetch_board_lists import (
    TrelloListRepsonse,
    trello_fetch_board_lists,
)

pytestmark = PYTEST_INTEGRATION_MARKER


def test_fetches_board_lists() -> None:
    lists = trello_fetch_board_lists(PLANNING_BOARD_ID)
    validate_keys(lists[0], TrelloListRepsonse)
    display("Lists:")
    display("\n".join([f"  {board_list['name']}" for board_list in lists]))
    assert_yes("Does the above match the open lists on the Planning board?")
