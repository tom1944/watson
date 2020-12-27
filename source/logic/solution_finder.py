import math
import time
from typing import List, Dict

from source.data.card import Card, Category
from source.data.knowledge import Knowledge
from source.data.knowledge_table import KnowledgeTable
from source.data.player import Player
from source.data.clues import Clues
from source.logic.check_knowledge import check_knowledge


class SolutionFinder:
    def __init__(self, clues: Clues, knowledge_table: KnowledgeTable):
        self.clues = clues
        self.context = clues.get_context()
        self.knowledge_table = knowledge_table
        self.available_players_for_card = {}
        self.player_hands = {}
        self.start_time = time.time()

    def find_possible_solution(self, timeout_sec=math.inf):
        self.start_time = time.time()

        if not check_knowledge(self.knowledge_table, self.clues):
            return None

        player_hands, murder_cards, free_cards = self.knowledge_table.current_player_hands()
        self.player_hands = player_hands
        self.available_players_for_card = self.find_available_players_for_card()
        murder_weapons, murder_rooms, murder_characters = self.possible_murder_cards(free_cards, murder_cards)
        for murder_weapon in murder_weapons:
            for murder_room in murder_rooms:
                for murder_character in murder_characters:
                    new_free_cards = [c for c in free_cards if c not in [murder_character, murder_weapon, murder_room]]
                    possible_player_hands = self._possible_solution(self.player_hands.copy(), new_free_cards,
                                                                    timeout_sec)
                    if possible_player_hands is not None:
                        return [murder_character, murder_weapon, murder_room], possible_player_hands
        return None

    def possible_murder_cards(self, free_cards: List[Card], known_murder_cards: List[Card]):
        murder_weapons = self._possible_murder_cards_in_category(free_cards, known_murder_cards, Category.WEAPON)
        murder_rooms = self._possible_murder_cards_in_category(free_cards, known_murder_cards, Category.ROOM)
        murder_characters = self._possible_murder_cards_in_category(free_cards, known_murder_cards, Category.CHARACTER)
        return murder_weapons, murder_rooms, murder_characters

    def _possible_murder_cards_in_category(self, free_cards: List[Card],
                                           known_murder_cards: List[Card], category: Category):
        if category in [c.category for c in known_murder_cards]:
            return [c for c in known_murder_cards if c.category == category]
        return [c for c in free_cards if c.category == category]

    def find_available_players_for_card(self) -> Dict[Player, List[Card]]:
        available_players_for_card = {c: [] for c in self.context.cards}
        for card in self.context.cards:
            for player in self.context.players:
                if self.knowledge_table.get(player, card) == Knowledge.MAYBE:
                    available_players_for_card[card].append(player)
        return available_players_for_card

    def _possible_solution(self, player_hands: Dict[Player, List[Card]], cards_left: List[Card], timeout_sec):
        if (time.time()-self.start_time) > timeout_sec:
            raise SolutionFinderTimeoutError()

        if len(cards_left) == 0:
            return player_hands

        card_to_give = cards_left[len(cards_left) - 1]
        for player in self.available_players_for_card[card_to_give]:
            if len(player_hands[player]) < player.cardAmount:
                player_hands[player].append(card_to_give)
                cards_left.remove(card_to_give)
                if check_knowledge(self.knowledge_table, self.clues, player_hands):
                    possible_player_hands = self._possible_solution(player_hands, cards_left, timeout_sec)
                    if possible_player_hands is not None:
                        return possible_player_hands
                player_hands[player].remove(card_to_give)
                cards_left.append(card_to_give)
        return None


class SolutionFinderTimeoutError(Exception):
    pass
