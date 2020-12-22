from typing import List, NamedTuple

from source.data.card import Card
from source.data.player import Player


class Context(NamedTuple):
    players: List[Player]
    cards: List[Card]

    def other_players(self, player: Player) -> List[Player]:
        return [p for p in self.players if p is not player]
