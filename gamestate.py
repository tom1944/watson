from typing import List, NamedTuple, Tuple

from knowledge import Knowledge
from player import Player
from card import Card


class Rumour(NamedTuple):
    claimer: Player
    weapon: Card
    room: Card
    suspect: Card
    replies: List[Tuple[Player, Knowledge]]

    def get_cards(self):
        return [self.weapon, self.room, self.suspect]


class GameState:
    def __init__(self, players: List[Player], cards: List[Card]):
        self.players = players
        self.knowledge_tables = []  # todo: init tables
        self.rumours = []

    def add_rumour(self, rumour):
        # todo: stub
        pass

    def add_card(self, player: Player, card: Card):
        # todo: stub
        pass
