from itertools import combinations
from typing import Dict, List

from card import Category, Card
from check_knowledge import check_knowledge
from knowledge import Knowledge
from knowledge_table import KnowledgeTable
from player import Player
from session import Session


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
        available_cards = {}
        cards_owned = {}
        player_hands = {}
        for player in self.context.players:
            available_cards[player] = []
            player_hands[player] = []
            cards_owned[player] = 0
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
