from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.constants import TRELLO_API_BASE_URL
from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.trello_api_authorization_headers import (
    trello_api_authorization_headers,
)
from pl_tiny_clients.trello_fetch_board_lists import TrelloId


@MockInUnitTests(MockReason.UNINVESTIGATED)
def trello_move_card(card_id: TrelloId, to_list_id: TrelloId) -> None:
    # Docs: https://developer.atlassian.com/cloud/trello/rest
    path = f"cards/{card_id}"
    requests_wrapper(
        f"{TRELLO_API_BASE_URL}/{path}",
        method="PUT",
        body_params={"idList": to_list_id},
        headers=trello_api_authorization_headers(),
    )
