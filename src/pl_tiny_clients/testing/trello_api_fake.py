from enum import Enum, auto
from typing import TypedDict
from uuid import uuid4

from pl_mocks_and_fakes import Fake, fake_for, mock_for

from pl_tiny_clients.trello_archive_card import trello_archive_card
from pl_tiny_clients.trello_create_card import trello_create_card
from pl_tiny_clients.trello_create_card_checklist import trello_create_card_checklist
from pl_tiny_clients.trello_create_checklist_item import trello_create_checklist_item
from pl_tiny_clients.trello_fetch_board_lists import (
    TrelloId,
    TrelloListRepsonse,
    trello_fetch_board_lists,
)
from pl_tiny_clients.trello_fetch_card import trello_fetch_card
from pl_tiny_clients.trello_fetch_card_checklists import (
    TrelloChecklistResponse,
    TrelloFetchCardChecklistsResponse,
    trello_fetch_card_checklists,
)
from pl_tiny_clients.trello_fetch_list_cards import (
    TrelloCardResponse,
    TrelloFetchListCardsResponse,
    trello_fetch_list_cards,
)
from pl_tiny_clients.trello_move_card import trello_move_card


class FakeChecklist(TypedDict):
    id: TrelloId
    items: list[str]


def fake_checklist() -> FakeChecklist:
    return {"id": str(uuid4()), "items": []}


class FakeCard(TypedDict):
    id: TrelloId
    name: str
    desc: str
    checklists: list[FakeChecklist]
    labels: list[str]  # The ID of the label


def fake_card() -> FakeCard:
    return {"id": str(uuid4()), "name": "", "desc": "", "checklists": [], "labels": []}


def _fake_card_to_trello_card_response(card: FakeCard) -> TrelloCardResponse:
    return {
        "id": card["id"],
        "name": card["name"],
        "desc": card["desc"],
        "labels": [{"id": label} for label in card["labels"]],
    }


def _fake_checklist_to_trello_checklist_response(
    checklist: FakeChecklist,
) -> TrelloChecklistResponse:
    return {
        "id": checklist["id"],
        "checkItems": [{"name": i} for i in checklist["items"]],
    }


class FakeList(TypedDict):
    id: TrelloId
    name: str
    cards: list[FakeCard]


def fake_list() -> FakeList:
    return {"id": str(uuid4()), "name": "", "cards": []}


class FakeBoard(TypedDict):
    id: TrelloId
    lists: list[FakeList]


type TrelloApiFakeState = list[FakeBoard]


class ConfigurableException(Enum):
    FETCH_BOARD_LISTS = auto()
    FETCH_LIST_CARDS = auto()
    FETCH_CARD = auto()
    CREATE_CARD = auto()
    ARCHIVE_CARD = auto()
    MOVE_CARD = auto()
    FETCH_CARD_CHECKLISTS = auto()
    CREATE_CARD_CHECKLIST = auto()
    CREATE_CHECKLIST_ITEM = auto()


class ConfiguredExceptionError(Exception):
    pass


class TrelloApiFake(Fake):
    def __init__(self) -> None:
        def _trello_fetch_board_lists_side_effect(
            board_id: TrelloId,
        ) -> list[TrelloListRepsonse]:
            if ConfigurableException.FETCH_BOARD_LISTS in self.configured_exceptions:
                raise ConfiguredExceptionError

            for board in self.boards:
                if board["id"] == board_id:
                    return [
                        {"id": fake_list["id"], "name": fake_list["name"]}
                        for fake_list in board["lists"]
                    ]
            msg = f"Board with id `{board_id}` not found."
            raise Exception(msg)

        def _trello_fetch_list_cards_side_effect(
            list_id: TrelloId,
        ) -> TrelloFetchListCardsResponse:
            if ConfigurableException.FETCH_LIST_CARDS in self.configured_exceptions:
                raise ConfiguredExceptionError

            return [
                _fake_card_to_trello_card_response(c)
                for c in self._fetch_list(list_id)["cards"]
            ]

        def _trello_fetch_card_side_effect(card_id: TrelloId) -> TrelloCardResponse:
            if ConfigurableException.FETCH_CARD in self.configured_exceptions:
                raise ConfiguredExceptionError

            return _fake_card_to_trello_card_response(self._fetch_card(card_id))

        def _trello_create_card_side_effect(
            list_id: TrelloId, name: str, description: str | None = None
        ) -> TrelloCardResponse:
            if ConfigurableException.CREATE_CARD in self.configured_exceptions:
                raise ConfiguredExceptionError

            card: FakeCard = {
                "id": str(uuid4()),
                "name": name,
                "desc": description if description is not None else "",
                "labels": [],
                "checklists": [],
            }

            self._fetch_list(list_id)["cards"].append(card)

            return _fake_card_to_trello_card_response(card)

        def _trello_archive_card_side_effect(card_id: TrelloId) -> None:
            if ConfigurableException.ARCHIVE_CARD in self.configured_exceptions:
                raise ConfiguredExceptionError

            self._remove_card_from_list(card_id)

        def _trello_move_card_side_effect(
            card_id: TrelloId, to_list_id: TrelloId
        ) -> None:
            if ConfigurableException.MOVE_CARD in self.configured_exceptions:
                raise ConfiguredExceptionError

            card = self._fetch_card(card_id)
            self._remove_card_from_list(card_id)
            to_list = self._fetch_list(to_list_id)
            to_list["cards"].append(card)

        def _trello_fetch_card_checklists_side_effect(
            card_id: TrelloId,
        ) -> TrelloFetchCardChecklistsResponse:
            if (
                ConfigurableException.FETCH_CARD_CHECKLISTS
                in self.configured_exceptions
            ):
                raise ConfiguredExceptionError

            return [
                _fake_checklist_to_trello_checklist_response(c)
                for c in self._fetch_card(card_id)["checklists"]
            ]

        def _trello_create_card_checklist_side_effect(
            card_id: TrelloId,
            name: str,  # noqa: ARG001
        ) -> TrelloChecklistResponse:
            if (
                ConfigurableException.CREATE_CARD_CHECKLIST
                in self.configured_exceptions
            ):
                raise ConfiguredExceptionError

            checklist: FakeChecklist = {"id": str(uuid4()), "items": []}
            self._fetch_card(card_id)["checklists"].append(checklist)
            return _fake_checklist_to_trello_checklist_response(checklist)

        def _trello_create_checklist_item_side_effect(
            checklist_id: TrelloId, name: str
        ) -> None:
            if (
                ConfigurableException.CREATE_CHECKLIST_ITEM
                in self.configured_exceptions
            ):
                raise ConfiguredExceptionError

            self._fetch_checklist(checklist_id)["items"].append(name)

        self.boards: list[FakeBoard] = []
        self.configured_exceptions: list[ConfigurableException] = []

        mock_for(
            trello_fetch_board_lists
        ).side_effect = _trello_fetch_board_lists_side_effect
        mock_for(
            trello_fetch_list_cards
        ).side_effect = _trello_fetch_list_cards_side_effect
        mock_for(trello_fetch_card).side_effect = _trello_fetch_card_side_effect
        mock_for(trello_create_card).side_effect = _trello_create_card_side_effect
        mock_for(trello_archive_card).side_effect = _trello_archive_card_side_effect
        mock_for(trello_move_card).side_effect = _trello_move_card_side_effect
        mock_for(
            trello_fetch_card_checklists
        ).side_effect = _trello_fetch_card_checklists_side_effect
        mock_for(
            trello_create_card_checklist
        ).side_effect = _trello_create_card_checklist_side_effect
        mock_for(
            trello_create_checklist_item
        ).side_effect = _trello_create_checklist_item_side_effect

    def fetch_board_lists(self, board_id: TrelloId) -> list[TrelloListRepsonse]:
        return mock_for(trello_fetch_board_lists)(board_id)

    def fetch_list_cards(self, list_id: TrelloId) -> TrelloFetchListCardsResponse:
        return mock_for(trello_fetch_list_cards)(list_id)

    def fetch_card(self, card_id: TrelloId) -> TrelloCardResponse:
        return mock_for(trello_fetch_card)(card_id)

    def create_card(
        self, list_id: TrelloId, name: str, description: str | None = None
    ) -> TrelloCardResponse:
        return mock_for(trello_create_card)(list_id, name, description)

    def archive_card(self, card_id: TrelloId) -> None:
        return mock_for(trello_archive_card)(card_id)

    def move_card(self, card_id: TrelloId, to_list_id: TrelloId) -> None:
        return mock_for(trello_move_card)(card_id, to_list_id)

    def fetch_card_checklists(
        self, card_id: TrelloId
    ) -> TrelloFetchCardChecklistsResponse:
        return mock_for(trello_fetch_card_checklists)(card_id)

    def create_card_checklist(
        self, card_id: TrelloId, name: str
    ) -> TrelloChecklistResponse:
        return mock_for(trello_create_card_checklist)(card_id, name)

    def create_checklist_item(self, checklist_id: TrelloId, name: str) -> None:
        return mock_for(trello_create_checklist_item)(checklist_id, name)

    def _fetch_list(self, list_id: TrelloId) -> FakeList:
        for board in self.boards:
            for fake_list in board["lists"]:
                if fake_list["id"] == list_id:
                    return fake_list
        msg = f"List with id `{list_id}` not found."
        raise Exception(msg)

    def _fetch_list_containing_card(self, card_id: TrelloId) -> FakeList:
        for board in self.boards:
            for fake_list in board["lists"]:
                for card in fake_list["cards"]:
                    if card["id"] == card_id:
                        return fake_list
        msg = f"Card with id `{card_id}` not found."
        raise Exception(msg)

    def _fetch_card(self, card_id: TrelloId) -> FakeCard:
        for board in self.boards:
            for fake_list in board["lists"]:
                for card in fake_list["cards"]:
                    if card["id"] == card_id:
                        return card
        msg = f"Card with id `{card_id}` not found."
        raise Exception(msg)

    def _fetch_checklist(self, checklist_id: TrelloId) -> FakeChecklist:
        for board in self.boards:
            for fake_list in board["lists"]:
                for card in fake_list["cards"]:
                    for checklist in card["checklists"]:
                        if checklist["id"] == checklist_id:
                            return checklist
        msg = f"Checklist with id `{checklist_id}` not found."
        raise Exception(msg)

    def _remove_card_from_list(self, card_id: TrelloId) -> None:
        fake_list = self._fetch_list_containing_card(card_id)
        fake_list["cards"] = [c for c in fake_list["cards"] if c["id"] != card_id]

    def set_up_fake(
        self,
        state: TrelloApiFakeState,
        configured_exceptions: list[ConfigurableException],
    ) -> None:
        self.boards = state
        self.configured_exceptions = configured_exceptions


def set_up_fake_trello(
    trello_fake: TrelloApiFake,
    state: TrelloApiFakeState,
    configured_exceptions: list[ConfigurableException] | None = None,
) -> None:
    if configured_exceptions is None:
        configured_exceptions = []
    trello_fake.set_up_fake(state, configured_exceptions)


def trello_api_fake() -> TrelloApiFake:
    return fake_for(TrelloApiFake)
