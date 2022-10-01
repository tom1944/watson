from typing import NamedTuple, List, Tuple

from source.domain.card import Card
from source.domain.knowledge import Knowledge
from source.domain.player import Player


class Rumour(NamedTuple):
    claimer: Player
    rumour_cards: List[Card]
    replies: List[Tuple[Player, Knowledge]]
