from typing import Dict, List

from card import Card
from context import Context
from player import Player
from rumour import Rumour


class Session:
    context: Context
    cards_seen: Dict[Player, List[Card]]
    rumours: List[Rumour]

    def __init__(self, context: Context, cards_seen: Dict[Player, List[Card]], rumours: List[Rumour]):
        self.context = context
        self.cards_seen = cards_seen
        self.rumours = rumours

    def get_cards(self, player: Player):
        return self.cards_seen[player]

    def get_rumours(self):
        return self.rumours

    def get_context(self):
        return self.context

    def add_card(self, card: Card, player: Player):
        self.cards_seen[player].append(card)

    def add_rumour(self, rumour: Rumour):
        self.rumours.append(rumour)

    def __eq__(self, other):
        return self.rumours == other.rumours and self.cards_seen == other.cards_seen
