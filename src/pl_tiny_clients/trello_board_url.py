from pl_tiny_clients.trello_fetch_board_lists import TrelloId


def trello_board_url(board_id: TrelloId) -> str:
    return f"https://trello.com/b/{board_id}"
