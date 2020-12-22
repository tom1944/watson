from typing import Dict, List

from card import Card
from context import Context
from knowledge import Knowledge
from player import Player

Clause = List[Card]


class Clauses:
    clauses = Dict[Player, List[Clause]]

    def __init__(self, context: Context):
        self.context = context
        self.clauses = {p: [] for p in context.players}

    def add_false_knowledge(self, player: Player, card: Card):
        self.remove_card_from_clauses(player, card)
        self.remove_empty_clauses()

    def add_true_knowledge(self, player, card):
        self.empty_clause_that_has_card(player, card)
        for other_player in self.context.other_players(player):
            self.remove_card_from_clauses(other_player, card)
        self.remove_empty_clauses()

    def remove_empty_clauses(self):
        for player in self.context.players:
            self.clauses[player] = list(filter(lambda a: a != [], self.clauses[player]))

    def empty_clause_that_has_card(self, player: Player, card: Card):
        for clause in self.get_clauses(player):
            if card in clause:
                clause.clear()
                
    def remove_card_from_clauses(self, player: Player, card: Card):
        for clause in self.get_clauses(player):
            if card in clause:
                clause.remove(card)

    def add_clause(self, player: Player, clause: List[Card]):
        self.clauses[player].append(clause)

    def get_clauses(self, player: Player):
        return self.clauses[player]
