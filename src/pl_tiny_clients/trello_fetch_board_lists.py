from typing import TypedDict

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.constants import TRELLO_API_BASE_URL
from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.trello_api_authorization_headers import (
    trello_api_authorization_headers,
)

TrelloId = str


class TrelloListRepsonse(TypedDict):
    name: str
    id: TrelloId


@MockInUnitTests(MockReason.UNINVESTIGATED)
def trello_fetch_board_lists(board_id: TrelloId) -> list[TrelloListRepsonse]:
    # Docs: https://developer.atlassian.com/cloud/trello/rest

    path = f"board/{board_id}/lists"
    return requests_wrapper(
        f"{TRELLO_API_BASE_URL}/{path}",
        list[TrelloListRepsonse],
        query_params={"filter": "open"},
        headers=trello_api_authorization_headers(),
    )
