from source.data.context import Context
from source.io.knowledge_table_formatter import KnowledgeTableFormatter
from source.logic.brute_forcer import BruteForcer
from source.data.card import Card
from source.data.knowledge import Knowledge
from source.data.knowledge_table import KnowledgeTable
from source.data.player import Player
from source.data.rumour import Rumour
from source.data.clues import Clues
from source.logic.deriver import Deriver


class Watson:
    def __init__(self, context: Context):
        self.context = context
        self.clues = Clues(context)
        self.knowledge_table = KnowledgeTable(self.context.players, self.context.cards)
        self.brute_forcer = BruteForcer(self.clues, self.knowledge_table)
        self.deriver = Deriver(self.clues, self.knowledge_table)

    def add_knowledge(self, player: Player, card: Card, knowledge: Knowledge):
        self.clues.add_card(card, player)
        self.deriver.derive_from_new_knowledge(player, card, knowledge)
        self.brute_force_and_derive_from_findings()

    def add_rumour(self, rumour: Rumour) -> None:
        self.clues.add_rumour(rumour)
        self.deriver.derive_from_new_rumour(rumour)
        self.brute_force_and_derive_from_findings()

    def brute_force_and_derive_from_findings(self):
        for player in self.context.players:
            for card in self.context.cards:
                if self.knowledge_table.get(player, card) == Knowledge.MAYBE:
                    knowledge = self.brute_forcer.brute_force_on_card(player, card)
                    if knowledge != Knowledge.MAYBE:
                        self.deriver.derive_from_new_knowledge(player, card, knowledge)

    def display_state(self):
        formatter = KnowledgeTableFormatter()
        formatted_table = formatter.format_knowledge_table(self.knowledge_table)
        print(formatted_table)

    def get_knowledge_table(self) -> KnowledgeTable:
        return self.knowledge_table

    def get_context(self) -> Context:
        return self.context
