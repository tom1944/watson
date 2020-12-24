from source.data.card import Card
from source.data.knowledge import Knowledge
from source.data.knowledge_table import KnowledgeTable
from source.data.player import Player
from source.data.session import Session
from source.logic.solution_finder import SolutionFinder


class BruteForcer:
    def __init__(self, session: Session, knowledge_table: KnowledgeTable):
        self.session = session
        self.context = session.context
        self.knowledge_table = knowledge_table
        self.solution_finder = SolutionFinder(session, knowledge_table)

    def brute_force_on_card(self, player: Player, card: Card) -> Knowledge:
        if self.must_be_true(player, card):
            return Knowledge.TRUE
        if self.must_be_false(player, card):
            return Knowledge.FALSE
        return Knowledge.MAYBE

    def must_be_true(self, player: Player, card: Card) -> bool:
        self.knowledge_table.set(player, card, Knowledge.FALSE)
        can_be_false = self.has_solution()
        self.knowledge_table.set_forcefully(player, card, Knowledge.MAYBE)
        return not can_be_false

    def must_be_false(self, player: Player, card: Card) -> bool:
        self.knowledge_table.set(player, card, Knowledge.TRUE)
        can_be_true = self.has_solution()
        self.knowledge_table.set_forcefully(player, card, Knowledge.MAYBE)
        return not can_be_true

    def has_solution(self):
        if self.solution_finder.find_possible_solution() is None:
            return False
        else:
            return True
