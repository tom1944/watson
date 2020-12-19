from itertools import combinations
from typing import Dict, List

from card import Category, Card
from context import Context
from knowledge import Knowledge
from knowledge_table import KnowledgeTable
from player import Player
from session import Session


class BruteForcer:
    def __init__(self, context: Context, session: Session, knowledge_table: KnowledgeTable):
        self.context = context
        self.session = session
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
            if self.smart_check_knowledge(player_hands, new_unknown_cards):
                if player_index == len(self.context.players) - 1:
                    return True
                elif self._has_solution(player_hands, new_unknown_cards, available_cards, cards_owned,
                                        player_index + 1):
                    return True
                else:
                    player_hands[self.context.players[player_index + 1]] = []
        return False

    def smart_check_knowledge(self, player_hands: Dict[Player, List[Card]], unknown_cards: List[Card]):
        already_owned = {}
        for player in self.context.players:
            already_owned[player] = []
            for card in self.context.cards:
                if self.knowledge_table.get(player, card) == Knowledge.TRUE:
                    already_owned[player].append(card)
            if len(player_hands[player]+already_owned[player]) > player.cardAmount:
                return False

        for rumour in self.session.rumours:
            rumour_cards = rumour.rumour_cards
            for replier, knowledge in rumour.replies:
                possible_no_possession = set(rumour_cards).isdisjoint(player_hands[replier]+already_owned[replier])
                if knowledge == Knowledge.FALSE:
                    # Replier should not have any of the rumoured cards
                    if not possible_no_possession:
                        return False
                else:
                    # Replier should have any of the rumoured cards
                    if replier.cardAmount == len(player_hands[replier]+already_owned[replier])\
                            and possible_no_possession:
                        return False
                    if set(rumour_cards).isdisjoint(unknown_cards) and possible_no_possession:
                        return False
        return True

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
