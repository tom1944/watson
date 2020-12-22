from typing import List, Dict, Set

from card import Card
from knowledge import Knowledge
from knowledge_table import KnowledgeTable
from player import Player
from rumour import Rumour
from session import Session
from test.clauses import Clauses


class Deriver:
    def __init__(self, session: Session, knowledge_table: KnowledgeTable):
        self.session = session
        self.context = session.context
        self.knowledge_table = knowledge_table
        self.clauses = Clauses(self.context)

    def inspect_clauses(self):
        for player in self.context.players:
            for clause in self.clauses.get_clauses(player):
                if len(clause) == 1:
                    self.set_and_derive_true_knowledge_if_new(player, clause[0])

    def derive_from_new_rumour(self, rumour: Rumour):
        for replier, knowledge in rumour.replies:
            if knowledge == Knowledge.FALSE:
                for card in rumour.rumour_cards:
                    self.set_and_derive_false_knowledge_if_new(replier, card)
            elif knowledge == Knowledge.TRUE:
                clause = self.create_clause(replier, rumour.rumour_cards)
                if len(clause) > 1:
                    self.clauses.add_clause(replier, clause)
                elif len(clause) == 1:
                    self.set_and_derive_true_knowledge_if_new(replier, clause[0])

    def create_clause(self, player: Player, rumour_cards: List[Card]) -> List[Card]:
        clause = []
        for card in rumour_cards:
            if self.knowledge_table.get(player, card) == Knowledge.TRUE:
                return []
            elif self.knowledge_table.get(player,card) == Knowledge.MAYBE:
                clause.append(card)
        return clause

    def derive_from_new_knowledge(self, player: Player, card: Card):
        knowledge = self.knowledge_table.get(player, card)

        if knowledge == Knowledge.TRUE:
            self.derive_new_true_knowledge(player, card)
        elif knowledge == Knowledge.FALSE:
            self.derive_new_false_knowledge(player, card)
        else:
            raise DeriveCalledOnMaybeError("Value in knowledge table was Knowledge.Maybe")
        self.inspect_clauses()

    def set_and_derive_true_knowledge_if_new(self, player: Player, card: Card):
        if self.knowledge_table.get(player, card) != Knowledge.TRUE:
            self.knowledge_table.set(player, card, Knowledge.TRUE)
            self.derive_new_true_knowledge(player, card)

    def set_and_derive_false_knowledge_if_new(self, player: Player, card: Card):
        if self.knowledge_table.get(player, card) != Knowledge.FALSE:
            self.knowledge_table.set(player, card, Knowledge.FALSE)
            self.derive_new_false_knowledge(player, card)

    def derive_new_true_knowledge(self, player: Player, card: Card):
        self.clauses.add_true_knowledge(player, card)

        # Exclusion: Other players cannot have the same card
        for other_player in self.context.other_players(player):
            self.set_and_derive_false_knowledge_if_new(other_player, card)

        # Max cards: A player cannot have more cards than he has
        if self.nr_known_cards(player) == player.cardAmount:
            self.set_other_cards_to_false(player)

    def nr_known_cards(self, player) -> int:
        card_count = 0
        for card in self.context.cards:
            if self.knowledge_table.get(player, card) == Knowledge.TRUE:
                card_count += 1
        return card_count

    def set_other_cards_to_false(self, player):
        for card in self.context.cards:
            if self.knowledge_table.get(player, card) == Knowledge.MAYBE:
                self.set_and_derive_false_knowledge_if_new(player, card)

    def derive_new_false_knowledge(self, player: Player, card: Card):
        self.clauses.add_false_knowledge(player, card)
        return

    def get_clauses(self) -> Clauses:
        return self.clauses


class DeriveCalledOnMaybeError(Exception):
    pass
