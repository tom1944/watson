from typing import NamedTuple, List, Tuple

from card import Card
from knowledge import Knowledge
from player import Player


class Rumour(NamedTuple):
    claimer: Player
    weapon: Card
    room: Card
    suspect: Card
    replies: List[Tuple[Player, Knowledge]]

    def get_cards(self) -> List[Card]:
        return [self.weapon, self.room, self.suspect]