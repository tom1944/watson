from typing import List

from card import Card, Category
from context import Context
from player import Player


class Cards:
    MES = Card('Mes', Category.WEAPON)
    KANDELAAR = Card('Kandelaar', Category.WEAPON)
    PISTOOL = Card('Pistool', Category.WEAPON)
    VERGIF = Card('Vergif', Category.WEAPON)
    TROFFEE = Card('Troffee', Category.WEAPON)
    TOUW = Card('Touw', Category.WEAPON)
    KNUPPEL = Card('Knuppel', Category.WEAPON)
    BIJL = Card('Bijl', Category.WEAPON)
    HALTER = Card('Halter', Category.WEAPON)

    HAL = Card('Hal', Category.ROOM)
    EETKAMER = Card('Eetkamer', Category.ROOM)
    KEUKEN = Card('Keuken', Category.ROOM)
    TERRAS = Card('Terras', Category.ROOM)
    WERKKAMER = Card('Werkkamer', Category.ROOM)
    THEATER = Card('Theater', Category.ROOM)
    ZITKAMER = Card('Zitkamer', Category.ROOM)
    BUBBELBAD = Card('Bubbelbad', Category.ROOM)
    GASTENVERBLIJF = Card('Gastenverblijf', Category.ROOM)

    VANGEELEN = Card('Van Geelen', Category.CHARACTER)
    PIMPEL = Card('Pimpel', Category.CHARACTER)
    GROENEWOUD = Card('Groenewoud', Category.CHARACTER)
    BLAAUWVANDRAET = Card('Blaauw van Draet', Category.CHARACTER)
    ROODHART = Card('Roodhart', Category.CHARACTER)
    DEWIT = Card('De Wit', Category.CHARACTER)


def _make_cards() -> List[Card]:
    all_cards = list(_get_members_of_class(Cards))
    open_cards = [Cards.TROFFEE, Cards.TERRAS, Cards.VANGEELEN]
    return [c for c in all_cards if c not in open_cards]


def _get_members_of_class(cls):
    for property_name, value in vars(cls).items():
        if not _is_private_property(property_name):
            yield value


def _is_private_property(property_name: str):
    return property_name.startswith('_')


tom = Player("Tom", "Roodhart", 6)
menno = Player("Menno", "Blaauw van Draet", 6)
michiel = Player("Michiel", "De Wit", 6)


def _make_players() -> List[Player]:
    return [tom, menno, michiel]


context = Context(_make_players(), _make_cards())
