from typing import List, NamedTuple, Tuple

from knowledge import Knowledge
from player import Player
from card import Card
from card import Category


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
        self.cards = cards
        self.knowledge_tables = {}
        for category in Category:
            table = {}
            for player in players:
                column = {}
                for card in cards:
                    if card.category == category:
                        column[card] = Knowledge.MAYBE
                table[player] = column
            self.knowledge_tables[category] = table
        self.rumours = []

    def add_rumour(self, rumour):
        self.rumours.append(rumour)

    def add_card(self, player: Player, card: Card, knowledge: Knowledge):
        self.knowledge_tables[card.category][player][card] = knowledge
