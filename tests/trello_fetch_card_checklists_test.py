import webbrowser
from pprint import pprint

from pl_user_io.assert_yes import assert_yes
from pl_user_io.display import display
from pl_user_io.task import task

from pl_tiny_clients.constants import PLANNING_BOARD_ID, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.testing.validate_keys import validate_keys
from pl_tiny_clients.trello_board_url import trello_board_url
from pl_tiny_clients.trello_create_card import trello_create_card
from pl_tiny_clients.trello_create_card_checklist import trello_create_card_checklist
from pl_tiny_clients.trello_create_checklist_item import trello_create_checklist_item
from pl_tiny_clients.trello_fetch_board_lists import trello_fetch_board_lists
from pl_tiny_clients.trello_fetch_card_checklists import (
    TrelloChecklistItemResponse,
    TrelloChecklistResponse,
    trello_fetch_card_checklists,
)

pytestmark = PYTEST_INTEGRATION_MARKER


def test_fetch_card_checklists() -> None:
    lists = trello_fetch_board_lists(PLANNING_BOARD_ID)
    today_list = lists[0]
    card = trello_create_card(today_list["id"], "Test Card")
    checklist_create_response = trello_create_card_checklist(
        card["id"], "Test Checklist"
    )
    trello_create_checklist_item(checklist_create_response["id"], "Test Item")
    checklist = trello_fetch_card_checklists(card["id"])[0]
    validate_keys(checklist, TrelloChecklistResponse)
    validate_keys(checklist["checkItems"][0], TrelloChecklistItemResponse)
    webbrowser.open(trello_board_url(PLANNING_BOARD_ID))
    task("Find the card named 'Test Card' in the Today list.")
    display("Checklist:")
    pprint(checklist)
    assert_yes(
        "Does the above match the checklist on the card, including the checklist item?"
    )
    task("Manually delete the card named 'Test Card' created in the Today list.")
