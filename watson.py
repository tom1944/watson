from brute_forcer import BruteForcer
from card import Card
from knowledge import Knowledge
from knowledge_table import KnowledgeTable
from player import Player
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

    def count_cards(self, player) -> int:
        card_count = 0
        for card in self.context.cards:
            if self.knowledge_table.get(player, card) == Knowledge.TRUE:
                card_count += 1
        return card_count

    def get_knowledge_table(self) -> KnowledgeTable:
        return self.knowledge_table
