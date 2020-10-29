from typing import NamedTuple
from enum import Enum


class Category(Enum):
    CHARACTER = 'Character'
    WEAPON = 'Weapon'
    ROOM = 'Room'


class Card(NamedTuple):
    name: str
    category: Category


def cat_from_string(category_name: str) -> Category:
    for cat in Category:
        if category_name == cat.value:
            return cat
    raise Exception(f'Category name "{category_name}" invalid')


weaponNames = ['Mes', 'Kandelaar', 'Pistool', 'Vergif', 'Troffee', 'Touw', 'Knuppel', 'Bijl', 'Halter']
roomNames = ['Hal', 'Eetkamer', 'Keuken', 'Terras', 'Werkkamer', 'Theater', 'Zitkamer', 'Bubbelbad', 'Gastenverblijf']
characterNames = ["Van Geelen", "Pimpel", "Groenewoud", "Blaauw van Draet", "Roodhart", "De Wit"]

characterCards = [Card(c, Category.CHARACTER) for c in characterNames]
weaponCards = [Card(c, Category.WEAPON) for c in weaponNames]
roomCards = [Card(c, Category.ROOM) for c in roomNames]
allCards = characterCards + weaponCards + roomCards


