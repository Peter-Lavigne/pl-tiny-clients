from typing import TypedDict

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.constants import TRELLO_API_BASE_URL
from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.trello_api_authorization_headers import (
    trello_api_authorization_headers,
)
from pl_tiny_clients.trello_fetch_board_lists import TrelloId


class TrelloLabelResponse(TypedDict):
    id: TrelloId


class TrelloCardResponse(TypedDict):
    id: TrelloId
    name: str
    desc: str
    labels: list[TrelloLabelResponse]


type TrelloFetchListCardsResponse = list[TrelloCardResponse]


@MockInUnitTests(MockReason.UNINVESTIGATED)
def trello_fetch_list_cards(list_id: TrelloId) -> TrelloFetchListCardsResponse:
    # Docs: https://developer.atlassian.com/cloud/trello/rest
    path = f"list/{list_id}/cards"
    return requests_wrapper(
        f"{TRELLO_API_BASE_URL}/{path}",
        TrelloFetchListCardsResponse.__value__,
        headers=trello_api_authorization_headers(),
    )
