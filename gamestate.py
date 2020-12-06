from typing import List

from card import Card
from player import Player
from rumour import Rumour


class GameState:
    players: List[Player]
    your_cards: List[Card]
    cards: List[Card]
    rumours: List[Rumour]

    def __init__(self, players: List[Player], cards: List[Card], your_cards: List[Card]):
        self.players = players
        self.your_cards = your_cards
        self.cards = cards
        self.rumours = []
