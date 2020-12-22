from typing import NamedTuple, List, Tuple

from source.data.card import Card
from source.data.knowledge import Knowledge
from source.data.player import Player


class Rumour(NamedTuple):
    claimer: Player
    rumour_cards: List[Card]
    replies: List[Tuple[Player, Knowledge]]
