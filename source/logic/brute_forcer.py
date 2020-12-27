import math

from source.data.card import Card
from source.data.knowledge import Knowledge
from source.data.knowledge_table import KnowledgeTable
from source.data.player import Player
from source.data.clues import Clues
from source.logic.solution_finder import SolutionFinder, SolutionFinderTimeoutError


class BruteForcer:
    def __init__(self, clues: Clues, knowledge_table: KnowledgeTable):
        self._knowledge_table = knowledge_table
        self._solution_finder = SolutionFinder(clues, knowledge_table)

    def brute_force_on_card(self, player: Player, card: Card, timeout_sec=math.inf) -> Knowledge:
        try:
            return self._brute_force_on_card(card, player, timeout_sec)
        except SolutionFinderTimeoutError:
            self._knowledge_table.set_forcefully(player, card, Knowledge.MAYBE)
            raise BruteForceTimeoutError('Timed out on card: ' + card.name)

    def _brute_force_on_card(self, card, player, time_out_sec):
        if self._must_be_true(player, card, time_out_sec):
            return Knowledge.TRUE
        if self._must_be_false(player, card, time_out_sec):
            return Knowledge.FALSE
        return Knowledge.MAYBE

    def _must_be_true(self, player: Player, card: Card, time_out_sec) -> bool:
        self._knowledge_table.set(player, card, Knowledge.FALSE)
        can_be_false = self._has_solution(time_out_sec)
        self._knowledge_table.set_forcefully(player, card, Knowledge.MAYBE)
        return not can_be_false

    def _must_be_false(self, player: Player, card: Card, time_out_sec) -> bool:
        self._knowledge_table.set(player, card, Knowledge.TRUE)
        can_be_true = self._has_solution(time_out_sec)
        self._knowledge_table.set_forcefully(player, card, Knowledge.MAYBE)
        return not can_be_true

    def _has_solution(self, time_out_sec):
        if self._solution_finder.find_possible_solution(time_out_sec) is None:
            return False
        else:
            return True


class BruteForceTimeoutError(Exception):
    pass
