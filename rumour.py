from typing import NamedTuple, List, Tuple

from card import Card
from knowledge import Knowledge
from player import Player


class Rumour(NamedTuple):
    claimer: Player
    rumour_cards: List[Card]
    replies: List[Tuple[Player, Knowledge]]