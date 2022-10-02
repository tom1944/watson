from source.domain.card import Card
from source.domain.clues import Clues
from source.domain.context import Context
from source.domain.knowledge import Knowledge
from source.domain.knowledge_table import KnowledgeTable
from source.domain.player import Player
from source.domain.rumour import Rumour
from source.logic.brute_forcer import BruteForcer
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

    def add_info_from_clues(self, clues: Clues):
        self._add_cards_from_clues(clues)
        self._add_rumours_from_clues(clues)
        self.brute_force_and_derive_from_findings()

    def _add_cards_from_clues(self, clues):
        for player, cards in clues.cards_seen.items():
            for card in cards:
                self.clues.add_card(card, player)
                self.deriver.derive_from_new_knowledge(player, card, Knowledge.TRUE)

    def _add_rumours_from_clues(self, clues):
        for rumour in clues.get_rumours():
            self.clues.add_rumour(rumour)
            self.deriver.derive_from_new_rumour(rumour)

    def get_knowledge_table(self) -> KnowledgeTable:
        return self.knowledge_table

    def get_context(self) -> Context:
        return self.context

    def get_clues(self) -> Clues:
        return self.clues
