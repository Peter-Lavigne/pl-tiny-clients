from pl_tiny_clients.constants import PLANNING_BOARD_ID
from pl_tiny_clients.trello_board_url import trello_board_url


def test_trello_board_url() -> None:
    url = trello_board_url(PLANNING_BOARD_ID)

    assert url == "https://trello.com/b/aC1spZlt"  # pasted from browser
