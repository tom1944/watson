from typing import List, Tuple, Optional, Dict

import utility
from gamestate import GameState
from knowledge import Knowledge
from player import Player
from card import Card
from card import Category
from rumour import Rumour

KnowledgeTables = Dict[
    Category,
    Dict[
        Player,
        Dict[
            Card,
            Knowledge]
    ]
]    # typedef


class Watson:
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.knowledge_tables = {}
        for category in Category:
            table = {}
            for player in game_state.players:
                column = {}
                for card in game_state.used_cards:
                    if card.category == category:
                        column[card] = Knowledge.MAYBE
                table[player] = column
            self.knowledge_tables[category] = table
        self.game_state.rumours = []

    def add_knowledge(self, player: Player, card: Card, knowledge: Knowledge):
        self.derive_knowledge(player, card, knowledge)
        self.basic_brute_force()

    def derive_knowledge(self, player: Player, card: Card, knowledge: Knowledge):
        self.write_knowledge_safely(card, knowledge, player)

        # Exclusion: Other players cannot have the same card
        if knowledge == Knowledge.TRUE:  # Exclude other players if a player has a card
            for other_player in self.game_state.players:
                if other_player != player:
                    self.knowledge_tables[card.category][other_player][card] = Knowledge.FALSE

        # Max cards: A player cannot have more cards than he has
        for player in self.game_state.players:  # Count known cards
            card_amount = self.count_cards(player)
            if card_amount == player.cardAmount:
                for card in self.game_state.used_cards:
                    if self.knowledge_tables[card.category][player][card] == Knowledge.MAYBE:
                        self.add_knowledge(player, card, Knowledge.FALSE)

    def write_knowledge_safely(self, card, knowledge, player):
        if self.knowledge_tables[card.category][player][card] != Knowledge.MAYBE:
            if self.knowledge_tables[card.category][player][card] != knowledge:
                raise Exception(
                    f'Contradiction in table {card.category} player {player.name} card {card.name} '
                    f'Attempt to overwrite {self.knowledge_tables[card.category][player][card]} with {knowledge}'
                )
        self.knowledge_tables[card.category][player][card] = knowledge

    def basic_brute_force(self):
        # Brute force the knowledge table on the rumours
        for player in self.game_state.players:
            for card in self.game_state.used_cards:
                if self.knowledge_tables[card.category][player][card] == Knowledge.MAYBE:

                    self.knowledge_tables[card.category][player][card] = Knowledge.TRUE  # Try to fill in true
                    if not self.has_solution():
                        self.knowledge_tables[card.category][player][card] = Knowledge.MAYBE
                        self.add_knowledge(player, card, Knowledge.FALSE)
                        continue

                    self.knowledge_tables[card.category][player][card] = Knowledge.FALSE  # Try to fill in false
                    if not self.has_solution():
                        self.knowledge_tables[card.category][player][card] = Knowledge.MAYBE
                        self.add_knowledge(player, card, Knowledge.TRUE)
                    else:
                        self.knowledge_tables[card.category][player][card] = Knowledge.MAYBE

    def add_rumour(self, rumour: Rumour) -> None:
        self.game_state.rumours.append(rumour)
        for reply in rumour.replies:  # Set all cards to false if rumour is answered false
            player, knowledge = reply
            if knowledge == Knowledge.FALSE:
                for r_card in rumour.rumour_cards:
                    self.add_knowledge(player, r_card, Knowledge.FALSE)

    def has_solution(self) -> bool:
        return self.smart_has_solution()
        # Brute forces knowledge tables and checks the solution with the rumours, edits tables upon findings
        next_maybe = self.find_maybe()
        if next_maybe is None:  # Check the final solution
            return self.check_knowledge()

        category, player, card = next_maybe
        self.knowledge_tables[category][player][card] = Knowledge.TRUE  # Try true
        if self.check_knowledge():
            if self.has_solution():
                self.knowledge_tables[category][player][card] = Knowledge.MAYBE  # Reset
                return True

        self.knowledge_tables[category][player][card] = Knowledge.FALSE   # Try false
        if self.check_knowledge():
            if self.has_solution():
                self.knowledge_tables[category][player][card] = Knowledge.MAYBE  # Reset
                return True
        self.knowledge_tables[category][player][card] = Knowledge.MAYBE  # Reset
        return False

    def smart_has_solution(self) -> bool:
        unknown_cards = [c for c in self.game_state.used_cards if c not in self.known_cards()]
        available_cards = {}
        cards_owned = {}
        player_hands = {}
        for player in self.game_state.players:
            available_cards[player] = []
            player_hands[player] = []
            cards_owned[player] = 0
            for card in self.game_state.used_cards:
                if self.knowledge_tables[card.category][player][card] == Knowledge.MAYBE:
                    available_cards[player].append(card)
                elif self.knowledge_tables[card.category][player][card] == Knowledge.TRUE:
                    cards_owned[player] += 1

        choose_weapon = [c for c in unknown_cards if c.category == Category.WEAPON]
        choose_room = [c for c in unknown_cards if c.category == Category.ROOM]
        choose_character = [c for c in unknown_cards if c.category == Category.CHARACTER]
        for weapon in choose_weapon:
            for room in choose_room:
                for character in choose_character:
                    new_unknown_cards = [c for c in unknown_cards if c not in [character, weapon, room]]
                    if self._smart_has_solution(player_hands, new_unknown_cards, available_cards, cards_owned, 0):
                        return True
        return False

    def _smart_has_solution(self, player_hands: Dict[Player, List[Card]], unknown_cards: List[Card],
                            available_cards: Dict[Player, List[Card]], cards_owned: Dict[Player, int],
                            player_index: int) -> bool:
        player = self.game_state.players[player_index]
        player_hand = utility.permutations([c for c in unknown_cards if c in available_cards[player]],
                                           player.cardAmount-cards_owned[player])

        for hand in player_hand:
            player_hands[player] = hand
            new_unknown_cards = [c for c in unknown_cards if c not in hand]
            if self.smart_check_knowledge(player_hands, new_unknown_cards):
                if player_index == len(self.game_state.players) - 1:
                    return True
                elif self._smart_has_solution(player_hands, new_unknown_cards, available_cards, cards_owned,
                                              player_index + 1):
                    return True
                else:
                    player_hands[self.game_state.players[player_index + 1]] = []
        return False

    def check_knowledge(self) -> bool:
        # Checks whether given knowledge tables might comply with given rumours
        # Checks whether maximum number of cards is not exceeded

        for rumour in self.game_state.rumours:
            rumour_cards = rumour.rumour_cards
            for replier, knowledge in rumour.replies:
                if knowledge == Knowledge.FALSE:
                    # Replier should not have any of the rumoured cards
                    for rumour_card in rumour_cards:
                        if self.knowledge_tables[rumour_card.category][replier][rumour_card] == Knowledge.TRUE:
                            return False
                else:
                    # Replier should have any of the rumoured cards
                    true_or_maybe_found = False
                    for rumour_card in rumour_cards:
                        if self.knowledge_tables[rumour_card.category][replier][rumour_card] != Knowledge.FALSE:
                            true_or_maybe_found = True
                            break
                    if not true_or_maybe_found:
                        return False

        for player in self.game_state.players:
            card_amount = 0
            for card in self.game_state.used_cards:
                if self.knowledge_tables[card.category][player][card] == Knowledge.TRUE:
                    card_amount += 1
            if card_amount > player.cardAmount:
                return False
        return True

    def smart_check_knowledge(self, player_hands: Dict[Player, List[Card]], unknown_cards: List[Card]):
        already_owned = {}
        for player in self.game_state.players:
            already_owned[player] = []
            for card in self.game_state.used_cards:
                if self.knowledge_tables[card.category][player][card] == Knowledge.TRUE:
                    already_owned[player].append(card)
            if len(player_hands[player]+already_owned[player]) > player.cardAmount:
                return False

        for rumour in self.game_state.rumours:
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

    def find_maybe(self) -> Optional[Tuple[Category, Player, Card]]:
        for player in self.game_state.players:
            for card in self.game_state.used_cards:
                if self.knowledge_tables[card.category][player][card] == Knowledge.MAYBE:
                    return card.category, player, card
        return None

    def count_cards(self, player) -> int:
        card_count = 0
        for card in self.game_state.used_cards:
            if self.knowledge_tables[card.category][player][card] == Knowledge.TRUE:
                card_count += 1
        return card_count

    def known_cards(self) -> List[Card]:
        known_cards = []
        for player in self.game_state.players:
            for card in self.game_state.used_cards:
                if self.knowledge_tables[card.category][player][card] == Knowledge.TRUE:
                    known_cards.append(card)
        return known_cards
