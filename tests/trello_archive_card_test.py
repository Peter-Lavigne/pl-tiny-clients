from pl_user_io.assert_yes import assert_yes
from pl_user_io.task_with_url import task_with_url

from pl_tiny_clients.constants import PLANNING_BOARD_ID, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.trello_archive_card import trello_archive_card
from pl_tiny_clients.trello_board_url import trello_board_url
from pl_tiny_clients.trello_create_card import trello_create_card
from pl_tiny_clients.trello_fetch_board_lists import trello_fetch_board_lists

pytestmark = PYTEST_INTEGRATION_MARKER


def test_archive_card() -> None:
    lists = trello_fetch_board_lists(PLANNING_BOARD_ID)
    today_list = lists[0]
    card = trello_create_card(today_list["id"], "Test Card")
    task_with_url(
        "Open the card titled 'Test Card'", trello_board_url(PLANNING_BOARD_ID)
    )

    trello_archive_card(card["id"])

    assert_yes("Was that card archived?")
