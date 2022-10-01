from typing import List, NamedTuple

from source.domain.card import Card
from source.domain.player import Player


class Context(NamedTuple):
    players: List[Player]
    cards: List[Card]
    open_cards: List[Card]

    def other_players(self, player: Player) -> List[Player]:
        return [p for p in self.players if p is not player]
