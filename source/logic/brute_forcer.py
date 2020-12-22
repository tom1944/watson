from itertools import combinations
from typing import Dict, List, Optional, Tuple

from source.data.card import Category, Card
from source.logic.check_knowledge import check_knowledge
from source.data.knowledge import Knowledge
from source.data.knowledge_table import KnowledgeTable
from source.data.player import Player
from source.data.session import Session


class BruteForcer:
    def __init__(self, session: Session, knowledge_table: KnowledgeTable):
        self.session = session
        self.context = session.context
        self.knowledge_table = knowledge_table

    def known_cards(self) -> List[Card]:
        known_cards = []
        for player in self.context.players:
            for card in self.context.cards:
                if self.knowledge_table.get(player, card) == Knowledge.TRUE:
                    known_cards.append(card)
        return known_cards

    def has_solution(self) -> bool:
        unknown_cards = [c for c in self.context.cards if c not in self.known_cards()]
        available_cards = {p: [] for p in self.context.players}
        player_hands = {p: [] for p in self.context.players}
        cards_owned = {p: 0 for p in self.context.players}

        for player in self.context.players:
            for card in self.context.cards:
                if self.knowledge_table.get(player, card) == Knowledge.MAYBE:
                    available_cards[player].append(card)
                elif self.knowledge_table.get(player, card) == Knowledge.TRUE:
                    cards_owned[player] += 1

        choose_weapon = [c for c in unknown_cards if c.category == Category.WEAPON]
        choose_room = [c for c in unknown_cards if c.category == Category.ROOM]
        choose_character = [c for c in unknown_cards if c.category == Category.CHARACTER]
        for weapon in choose_weapon:
            for room in choose_room:
                for character in choose_character:
                    new_unknown_cards = [c for c in unknown_cards if c not in [character, weapon, room]]
                    if self._has_solution(player_hands, new_unknown_cards, available_cards, cards_owned, 0):
                        return True
        return False

    def _has_solution(self, player_hands: Dict[Player, List[Card]], unknown_cards: List[Card],
                      available_cards: Dict[Player, List[Card]], cards_owned: Dict[Player, int],
                      player_index: int) -> bool:
        player = self.context.players[player_index]
        player_hand = combinations([c for c in unknown_cards if c in available_cards[player]],
                                   player.cardAmount-cards_owned[player])

        for hand in player_hand:
            player_hands[player] = list(hand)
            new_unknown_cards = [c for c in unknown_cards if c not in hand]
            if check_knowledge(self.knowledge_table, self.session, player_hands):
                if player_index == len(self.context.players) - 1:
                    return True
                elif self._has_solution(player_hands, new_unknown_cards, available_cards, cards_owned,
                                        player_index + 1):
                    return True
                else:
                    player_hands[self.context.players[player_index + 1]] = []
        return False

    def basic_brute_force(self):
        # Brute force the knowledge table on the rumours
        for player in self.context.players:
            for card in self.context.cards:
                if self.knowledge_table.get(player, card) == Knowledge.MAYBE:

                    self.knowledge_table.set(player, card, Knowledge.TRUE)  # Try to fill in true
                    if not self.has_solution():
                        self.knowledge_table.set_forcefully(player, card, Knowledge.MAYBE)
                        self.knowledge_table.set(player, card, Knowledge.FALSE)
                        continue

                    self.knowledge_table.set(player, card, Knowledge.FALSE)  # Try to fill in false
                    if not self.has_solution():
                        self.knowledge_table.set_forcefully(player, card, Knowledge.MAYBE)
                        self.knowledge_table.set(player, card, Knowledge.TRUE)
                    else:
                        self.knowledge_table.set_forcefully(player, card, Knowledge.MAYBE)

    # Methods below are outdated but kept for reference to improve their new version
    def old_has_solution(self) -> bool:
        return self.has_solution()
        # Brute forces knowledge tables and checks the solution with the rumours, edits tables upon findings
        next_maybe = self.find_maybe()
        if next_maybe is None:  # Check the final solution
            return self.check_knowledge()

        category, player, card = next_maybe
        self.knowledge_table.set(player, card, Knowledge.TRUE)  # Try true
        if self.check_knowledge():
            if self.old_has_solution():
                self.knowledge_table.set(player, card, Knowledge.MAYBE)  # Reset
                return True

        self.knowledge_table.set(player, card, Knowledge.FALSE)  # Try false
        if self.check_knowledge():
            if self.old_has_solution():
                self.knowledge_table.set(player, card, Knowledge.MAYBE)  # Reset
                return True
        self.knowledge_table.set(player, card, Knowledge.MAYBE)  # Reset
        return False

    def find_maybe(self) -> Optional[Tuple[Category, Player, Card]]:
        for player in self.context.players:
            for card in self.context.cards:
                if self.knowledge_table.get(player, card) == Knowledge.MAYBE:
                    return card.category, player, card
        return None
