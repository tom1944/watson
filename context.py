from typing import List, NamedTuple

from card import Card
from player import Player


class Context(NamedTuple):
    players: List[Player]
    cards: List[Card]
