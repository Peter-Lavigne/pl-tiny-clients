import webbrowser

from pl_user_io.assert_yes import assert_yes
from pl_user_io.task import task

from pl_tiny_clients.constants import PLANNING_BOARD_ID, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.trello_board_url import trello_board_url
from pl_tiny_clients.trello_create_card import trello_create_card
from pl_tiny_clients.trello_create_card_checklist import trello_create_card_checklist
from pl_tiny_clients.trello_create_checklist_item import trello_create_checklist_item
from pl_tiny_clients.trello_fetch_board_lists import trello_fetch_board_lists

pytestmark = PYTEST_INTEGRATION_MARKER


def test_create_checklist_item() -> None:
    lists = trello_fetch_board_lists(PLANNING_BOARD_ID)
    today_list = lists[0]
    card = trello_create_card(today_list["id"], "Test Card")
    checklist = trello_create_card_checklist(card["id"], "Test Checklist")
    trello_create_checklist_item(checklist["id"], "Test Item")
    webbrowser.open(trello_board_url(PLANNING_BOARD_ID))
    assert_yes(
        "Was a checklist item named 'Test Item' created on a checklist named 'Test Checklist' on a card named 'Test Card' in the 'To Do' list on the Planning board?"
    )
    task("Manually delete the created card.")
