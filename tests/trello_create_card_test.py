import webbrowser
from pprint import pprint

from pl_user_io.assert_yes import assert_yes
from pl_user_io.display import display
from pl_user_io.task import task

from pl_tiny_clients.constants import PLANNING_BOARD_ID, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.testing.validate_keys import validate_keys
from pl_tiny_clients.trello_board_url import trello_board_url
from pl_tiny_clients.trello_create_card import trello_create_card
from pl_tiny_clients.trello_fetch_board_lists import trello_fetch_board_lists
from pl_tiny_clients.trello_fetch_list_cards import TrelloCardResponse

pytestmark = PYTEST_INTEGRATION_MARKER


def test_create_card() -> None:
    lists = trello_fetch_board_lists(PLANNING_BOARD_ID)
    today_list = lists[0]
    card = trello_create_card(today_list["id"], "Test Card", "Test description")
    validate_keys(card, TrelloCardResponse)
    webbrowser.open(trello_board_url(PLANNING_BOARD_ID))
    assert_yes(
        "Was a card 'Test Card' with description 'Test description' created in the 'To Do' list on the Planning board?"
    )
    display("Card data:")
    pprint(card)
    assert_yes("Does the return value above match the created card?")
    task("Manually delete the created card.")
