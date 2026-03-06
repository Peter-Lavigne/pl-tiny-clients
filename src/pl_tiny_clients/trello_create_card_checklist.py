from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.constants import TRELLO_API_BASE_URL
from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.trello_api_authorization_headers import (
    trello_api_authorization_headers,
)
from pl_tiny_clients.trello_fetch_board_lists import TrelloId
from pl_tiny_clients.trello_fetch_card_checklists import TrelloChecklistResponse


@MockInUnitTests(MockReason.UNINVESTIGATED)
def trello_create_card_checklist(
    card_id: TrelloId, name: str
) -> TrelloChecklistResponse:
    path = f"cards/{card_id}/checklists"
    # Docs: https://developer.atlassian.com/cloud/trello/rest
    # Beware: I rely on the returned "id", but according to the docs, "A schema has not been defined for this response code."
    # https://developer.atlassian.com/cloud/trello/rest/api-group-cards/#api-cards-id-checklists-post
    return requests_wrapper(
        f"{TRELLO_API_BASE_URL}/{path}",
        TrelloChecklistResponse,
        method="POST",
        body_params={"name": name},
        headers=trello_api_authorization_headers(),
    )
