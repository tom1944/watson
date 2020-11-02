from typing import List, NamedTuple, Tuple, Optional, Dict

import utility
from knowledge import Knowledge
from player import Player
from card import Card
from card import Category


KnowledgeTables = Dict[
    Category,
    Dict[
        Player,
        Dict[
            Card,
            Knowledge]
    ]
]    # typedef


class Rumour(NamedTuple):
    claimer: Player
    weapon: Card
    room: Card
    suspect: Card
    replies: List[Tuple[Player, Knowledge]]

    def get_cards(self):
        return [self.weapon, self.room, self.suspect]


class Watson:
    def __init__(self, players: List[Player], cards: List[Card]):
        self.players = players
        self.cards = cards
        self.knowledge_tables = {}
        for category in Category:
            table = {}
            for player in players:
                column = {}
                for card in cards:
                    if card.category == category:
                        column[card] = Knowledge.MAYBE
                table[player] = column
            self.knowledge_tables[category] = table
        self.rumours = []

    def add_knowledge(self, player: Player, card: Card, knowledge: Knowledge):
        self.derive_knowledge(player, card, knowledge)
        self.basic_brute_force()

    def derive_knowledge(self, player: Player, card: Card, knowledge: Knowledge):
        self.write_knowledge_safely(card, knowledge, player)

        # Exclusion: Other players cannot have the same card
        if knowledge == Knowledge.TRUE:  # Exclude other players if a player has a card
            for other_player in self.players:
                if other_player != player:
                    self.knowledge_tables[card.category][other_player][card] = Knowledge.FALSE

        # Max cards: A player cannot have more cards than he has
        for player in self.players:  # Count known cards
            card_amount = self.count_cards(player)
            if card_amount == player.cardAmount:
                for card in self.cards:
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
        for player in self.players:
            for card in self.cards:
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
        self.rumours.append(rumour)
        for reply in rumour.replies:  # Set all cards to false if rumour is answered false
            player, knowledge = reply
            if knowledge == Knowledge.FALSE:
                self.add_knowledge(player, rumour.weapon, knowledge)
                self.add_knowledge(player, rumour.room, knowledge)
                self.add_knowledge(player, rumour.suspect, knowledge)

    def has_solution(self) -> bool:
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
        unknown_cards = [c for c in self.cards if c not in self.known_cards]
        available_cards = {}
        cards_owned = {}
        for player in self.players:
            for card in self.cards:
                if self.knowledge_tables[card.category][player][card] == Knowledge.MAYBE:
                    available_cards[player].append(card)
                elif self.knowledge_tables[card.category][player][card] == Knowledge.TRUE:
                    cards_owned[player] += 1

        player_hands = {}

        choose_weapon = utility.permutations([c for c in unknown_cards if c.category == Category.WEAPON], 1)
        for weapon in choose_weapon:
            unknown_cards = [c for c in unknown_cards if c not in weapon]
            choose_room = utility.permutations([c for c in unknown_cards if c.category == Category.WEAPON], 1)
            for room in choose_room:
                unknown_cards = [c for c in unknown_cards if c not in room]
                choose_character = utility.permutations([c for c in unknown_cards if c.category == Category.WEAPON], 1)
                for character in choose_character:
                    unknown_cards = [c for c in unknown_cards if c not in character]
                    if self._smart_has_solution(player_hands, unknown_cards, available_cards, cards_owned,
                                                self.players[0]):
                        return True
        return False

    def _smart_has_solution(self, player_hands: Dict[Player, List[Card]], unknown_cards: List[Card],
                            available_cards: Dict[Player, List[Card]], cards_owned: Dict[Player, int],
                            player: Player):
        player_hand = utility.permutations([c for c in unknown_cards if c in available_cards[player]],
                                           player.cardAmount-cards_owned[player])
        player_index = 0
        for p in self.players:
            if player is p:
                break
            player_index += 1

        for hand in player_hand:
            player_hands[player] = hand
            unknown_cards = [c for c in unknown_cards if c not in hand]
            if player_index is len(self.players)-1:
                if self.smart_check_knowledge(player_hands):
                    return True
            elif self._smart_has_solution(player_hands, unknown_cards, available_cards, cards_owned,
                                          self.players[player_index + 1]):
                return True
        return False

    def check_knowledge(self) -> bool:
        # Checks whether given knowledge tables might comply with given rumours
        # Checks whether maximum number of cards is not exceeded

        for rumour in self.rumours:
            rumour_cards = rumour.get_cards()
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

        for player in self.players:
            card_amount = 0
            for card in self.cards:
                if self.knowledge_tables[card.category][player][card] == Knowledge.TRUE:
                    card_amount += 1
            if card_amount > player.cardAmount:
                return False
        return True

    def smart_check_knowledge(self, player_hands: Dict[Player, List[Card]]):
        for player in self.players:
            for card in self.cards:
                if self.knowledge_tables[card.category][player][card] == Knowledge.TRUE:
                    player_hands[player].append(card)

        for rumour in self.rumours:
            rumour_cards = rumour.get_cards()
            for replier, knowledge in rumour.replies:
                if knowledge == Knowledge.FALSE:
                    # Replier should not have any of the rumoured cards
                    if not set(rumour_cards).isdisjoint(player_hands[replier]):
                        return False
                else:
                    # Replier should have any of the rumoured cards
                    if set(rumour_cards).isdisjoint(player_hands[replier]):
                        return False

        for player in self.players:
            card_amount = len(player_hands[player])
            if card_amount > player.cardAmount:
                return False
        return True

    def find_maybe(self) -> Optional[Tuple[Category, Player, Card]]:
        for player in self.players:
            for card in self.cards:
                if self.knowledge_tables[card.category][player][card] == Knowledge.MAYBE:
                    return card.category, player, card
        return None

    def count_cards(self, player) -> int:
        card_count = 0
        for card in self.cards:
            if self.knowledge_tables[card.category][player][card] == Knowledge.TRUE:
                card_count += 1
        return card_count

    def known_cards(self) -> List[Card]:
        known_cards = []
        for player in self.players:
            for card in self.cards:
                if self.knowledge_tables[card.category][player][card] == Knowledge.TRUE:
                    known_cards.append(card)
        return known_cards