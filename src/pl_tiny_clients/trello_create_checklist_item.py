from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.constants import TRELLO_API_BASE_URL
from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.trello_api_authorization_headers import (
    trello_api_authorization_headers,
)
from pl_tiny_clients.trello_fetch_board_lists import TrelloId


@MockInUnitTests(MockReason.UNINVESTIGATED)
def trello_create_checklist_item(checklist_id: TrelloId, name: str) -> None:
    # Docs: https://developer.atlassian.com/cloud/trello/rest
    path = f"checklists/{checklist_id}/checkItems"
    requests_wrapper(
        f"{TRELLO_API_BASE_URL}/{path}",
        method="POST",
        body_params={"name": name},
        headers=trello_api_authorization_headers(),
    )
