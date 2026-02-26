from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.constants import TRELLO_API_BASE_URL
from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.trello_api_authorization_headers import (
    trello_api_authorization_headers,
)
from pl_tiny_clients.trello_fetch_board_lists import TrelloId
from pl_tiny_clients.trello_fetch_list_cards import TrelloCardResponse


@MockInUnitTests(MockReason.UNINVESTIGATED)
def trello_fetch_card(card_id: TrelloId) -> TrelloCardResponse:
    # Docs: https://developer.atlassian.com/cloud/trello/rest
    path = f"cards/{card_id}"
    return requests_wrapper(
        f"{TRELLO_API_BASE_URL}/{path}",
        TrelloCardResponse,
        headers=trello_api_authorization_headers(),
    )
