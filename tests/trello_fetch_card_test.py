from pl_user_io.str_input import str_input
from pl_user_io.task import task

from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.testing.validate_keys import validate_keys
from pl_tiny_clients.trello_fetch_card import trello_fetch_card
from pl_tiny_clients.trello_fetch_list_cards import (
    TrelloCardResponse,
    TrelloLabelResponse,
)

pytestmark = PYTEST_INTEGRATION_MARKER


def test_fetch_card() -> None:
    task(
        "Create a trello card with the title TEST, description DESCRIPTION, and any label."
    )
    card_id = str_input("What is the ID of the card you just created?")

    card = trello_fetch_card(card_id)

    validate_keys(card, TrelloCardResponse)
    validate_keys(card["labels"][0], TrelloLabelResponse)
    assert card["name"] == "TEST"
    assert card["desc"] == "DESCRIPTION"

    task("Archive the card.")
