from pl_user_io.assert_yes import assert_yes
from pl_user_io.display import display

from pl_tiny_clients.constants import PLANNING_BOARD_ID, PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.testing.validate_keys import validate_keys
from pl_tiny_clients.trello_fetch_board_lists import trello_fetch_board_lists
from pl_tiny_clients.trello_fetch_list_cards import (
    TrelloCardResponse,
    TrelloLabelResponse,
    trello_fetch_list_cards,
)

pytestmark = PYTEST_INTEGRATION_MARKER


def test_fetch_list_cards() -> None:
    lists = trello_fetch_board_lists(PLANNING_BOARD_ID)
    weekly_list = lists[-2]
    cards = trello_fetch_list_cards(weekly_list["id"])
    validate_keys(cards[0], TrelloCardResponse)
    validate_keys(cards[0]["labels"][0], TrelloLabelResponse)
    display("Cards:")
    display("\n".join([f"  {card['name']}" for card in cards[:3]]))
    assert_yes(
        "Does the above match the first three cards in the 'Weekly' list on the Planning board?"
    )
