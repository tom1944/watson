from source.data.card import Card
from source.data.knowledge import Knowledge
from source.data.knowledge_table import KnowledgeTable
from source.data.player import Player
from source.data.clues import Clues
from source.logic.solution_finder import SolutionFinder


class BruteForcer:
    def __init__(self, clues: Clues, knowledge_table: KnowledgeTable):
        self._knowledge_table = knowledge_table
        self._solution_finder = SolutionFinder(clues, knowledge_table)

    def brute_force_on_card(self, player: Player, card: Card) -> Knowledge:
        if self._must_be_true(player, card):
            return Knowledge.TRUE
        if self._must_be_false(player, card):
            return Knowledge.FALSE
        return Knowledge.MAYBE

    def _must_be_true(self, player: Player, card: Card) -> bool:
        self._knowledge_table.set(player, card, Knowledge.FALSE)
        can_be_false = self._has_solution()
        self._knowledge_table.set_forcefully(player, card, Knowledge.MAYBE)
        return not can_be_false

    def _must_be_false(self, player: Player, card: Card) -> bool:
        self._knowledge_table.set(player, card, Knowledge.TRUE)
        can_be_true = self._has_solution()
        self._knowledge_table.set_forcefully(player, card, Knowledge.MAYBE)
        return not can_be_true

    def _has_solution(self):
        if self._solution_finder.find_possible_solution() is None:
            return False
        else:
            return True
