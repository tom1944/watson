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

    def add_card(self, player: Player, card: Card, knowledge: Knowledge):
        category_table = self.knowledge_tables[card.category]
        if category_table[player][card] != knowledge: #Check if knowledge is new
            category_table[player][card] = knowledge
            if knowledge == Knowledge.TRUE:           #Exclude other players if a player has a card
                for other_player in self.players:
                    if other_player != player:
                        category_table[other_player][card] = Knowledge.FALSE

    def add_rumour(self, rumour):
        self.rumours.append(rumour)
        for reply in rumour.replies:    #Set all cards to false if rumour is answered false
            player, knowledge = reply
            if knowledge == knowledge.FALSE:
                self.add_card(player, rumour.weapon, knowledge)
                self.add_card(player, rumour.room, knowledge)
                self.add_card(player, rumour.character, knowledge)
        self.deduce()


    def deduce(self):
        #todo: add stub
        pass
