from typing import TypedDict

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.constants import TRELLO_API_BASE_URL
from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.trello_api_authorization_headers import (
    trello_api_authorization_headers,
)
from pl_tiny_clients.trello_fetch_board_lists import TrelloId


class TrelloChecklistItemResponse(TypedDict):
    name: str


class TrelloChecklistResponse(TypedDict):
    id: TrelloId
    checkItems: list[TrelloChecklistItemResponse]


type TrelloFetchCardChecklistsResponse = list[TrelloChecklistResponse]


@MockInUnitTests(MockReason.UNINVESTIGATED)
def trello_fetch_card_checklists(
    card_id: TrelloId,
) -> TrelloFetchCardChecklistsResponse:
    # Docs: https://developer.atlassian.com/cloud/trello/rest
    path = f"cards/{card_id}/checklists"
    return requests_wrapper(
        f"{TRELLO_API_BASE_URL}/{path}",
        TrelloFetchCardChecklistsResponse.__value__,
        headers=trello_api_authorization_headers(),
    )
