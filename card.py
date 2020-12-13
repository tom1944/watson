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
