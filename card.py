from typing import NamedTuple
from enum import Enum


class Category(Enum):
    CHARACTER = 'Character'
    WEAPON = 'Weapon'
    ROOM = 'Room'


class Card(NamedTuple):
    name: str
    category: Category


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


def cat_from_string(category_name: str) -> Category:
    for cat in Category:
        if category_name == cat.value:
            return cat
    raise Exception(f'Category name "{category_name}" invalid')
