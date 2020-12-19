from itertools import combinations
from typing import List, Tuple, Optional, Dict

from brute_forcer import BruteForcer
from context import Context
from knowledge import Knowledge
from knowledge_table import KnowledgeTable
from player import Player
from card import Card
from card import Category
from rumour import Rumour
from session import Session


class Watson:
    def __init__(self, session: Session):
        self.session = session
        self.context = session.context
        self.knowledge_table = KnowledgeTable(self.context.players, self.context.cards)
        self.brute_forcer = BruteForcer(self.session, self.knowledge_table)

    def add_knowledge(self, player: Player, card: Card, knowledge: Knowledge):
        self.derive_knowledge(player, card, knowledge)

    def derive_knowledge(self, player: Player, card: Card, knowledge: Knowledge):
        self.knowledge_table.set(player, card, knowledge)

        # Exclusion: Other players cannot have the same card
        if knowledge == Knowledge.TRUE:  # Exclude other players if a player has a card
            for other_player in self.context.players:
                if other_player != player:
                    self.knowledge_table.set(other_player, card, Knowledge.FALSE)

        # Max cards: A player cannot have more cards than he has
        for player in self.context.players:  # Count known cards
            card_amount = self.count_cards(player)
            if card_amount == player.cardAmount:
                for card in self.context.cards:
                    if self.knowledge_table.get(player, card) == Knowledge.MAYBE:
                        self.add_knowledge(player, card, Knowledge.FALSE)

    def add_rumour(self, rumour: Rumour) -> None:
        self.session.add_rumour(rumour)
        for reply in rumour.replies:  # Set all cards to false if rumour is answered false
            player, knowledge = reply
            if knowledge == Knowledge.FALSE:
                for r_card in rumour.rumour_cards:
                    self.add_knowledge(player, r_card, Knowledge.FALSE)

    def has_solution(self) -> bool:
        return self.brute_forcer.has_solution()
        # Brute forces knowledge tables and checks the solution with the rumours, edits tables upon findings
        next_maybe = self.find_maybe()
        if next_maybe is None:  # Check the final solution
            return self.check_knowledge()

        category, player, card = next_maybe
        self.knowledge_table.set(player, card, Knowledge.TRUE)  # Try true
        if self.check_knowledge():
            if self.has_solution():
                self.knowledge_table.set(player, card, Knowledge.MAYBE)  # Reset
                return True

        self.knowledge_table.set(player, card, Knowledge.FALSE)  # Try false
        if self.check_knowledge():
            if self.has_solution():
                self.knowledge_table.set(player, card, Knowledge.MAYBE)  # Reset
                return True
        self.knowledge_table.set(player, card, Knowledge.MAYBE)  # Reset
        return False

    def check_knowledge(self) -> bool:
        # Checks whether given knowledge tables might comply with given rumours
        # Checks whether maximum number of cards is not exceeded

        for rumour in self.session.rumours:
            rumour_cards = rumour.rumour_cards
            for replier, knowledge in rumour.replies:
                if knowledge == Knowledge.FALSE:
                    # Replier should not have any of the rumoured cards
                    for rumour_card in rumour_cards:
                        if self.knowledge_table.get(replier, rumour_card) == Knowledge.TRUE:
                            return False
                else:
                    # Replier should have any of the rumoured cards
                    true_or_maybe_found = False
                    for rumour_card in rumour_cards:
                        if self.knowledge_table.get(replier, rumour_card) != Knowledge.FALSE:
                            true_or_maybe_found = True
                            break
                    if not true_or_maybe_found:
                        return False

        for player in self.context.players:
            card_amount = 0
            for card in self.context.cards:
                if self.knowledge_table.get(player, card) == Knowledge.TRUE:
                    card_amount += 1
            if card_amount > player.cardAmount:
                return False
        return True

    def find_maybe(self) -> Optional[Tuple[Category, Player, Card]]:
        for player in self.context.players:
            for card in self.context.cards:
                if self.knowledge_table.get(player, card) == Knowledge.MAYBE:
                    return card.category, player, card
        return None

    def count_cards(self, player) -> int:
        card_count = 0
        for card in self.context.cards:
            if self.knowledge_table.get(player, card) == Knowledge.TRUE:
                card_count += 1
        return card_count

    def get_knowledge_table(self) -> KnowledgeTable:
        return self.knowledge_table
