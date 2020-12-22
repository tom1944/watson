from source.logic.brute_forcer import BruteForcer
from source.data.card import Card
from source.data.knowledge import Knowledge
from source.data.knowledge_table import KnowledgeTable
from source.data.player import Player
from source.data.rumour import Rumour
from source.data.session import Session
from source.logic.deriver import Deriver


class Watson:
    def __init__(self, session: Session):
        self.session = session
        self.context = session.context
        self.knowledge_table = KnowledgeTable(self.context.players, self.context.cards)
        self.brute_forcer = BruteForcer(self.session, self.knowledge_table)
        self.deriver = Deriver(self.session, self.knowledge_table)

    def add_knowledge(self, player: Player, card: Card, knowledge: Knowledge):
        self.session.add_card(card, player)
        self.deriver.derive_from_new_knowledge(player, card, knowledge)
        self.brute_force()

    def add_rumour(self, rumour: Rumour) -> None:
        self.session.add_rumour(rumour)
        self.deriver.derive_from_new_rumour(rumour)
        self.brute_force()

    def brute_force(self):
        for player, card, knowledge in self.brute_forcer.brute_force_generator():
            if knowledge != Knowledge.MAYBE:
                self.knowledge_table.set(player, card, knowledge)
                self.deriver.derive_from_new_knowledge(player, card, knowledge)

    def get_knowledge_table(self) -> KnowledgeTable:
        return self.knowledge_table
