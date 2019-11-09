from typing import NamedTuple
from enum import Enum


class Category(Enum):
    CHARACTER = 'Character'
    WEAPON = 'Weapon'
    ROOM = 'Room'


class Card(NamedTuple):
    name: str
    category: Category


weaponNames = ['mes', 'kandelaar', 'pistool', 'vergif', 'trofee', 'touw', 'knuppel', 'bijl', 'halter']
roomNames = ['hal', 'eetkamer', 'keuken', 'terras', 'werkkamer', 'theater', 'zitkamer', 'bubbelbad', 'gastenverblijf']
characterNames = ["Van Geelen", "Pimpel", "Groenewoud", "Blaauw van Draet", "Roodhart", "De Wit"]

characterCards = [Card(c, Category.CHARACTER) for c in characterNames]
weaponCards = [Card(c, Category.WEAPON) for c in weaponNames]
roomCards = [Card(c, Category.ROOM) for c in roomNames]
allCards = characterCards + weaponCards + roomCards


