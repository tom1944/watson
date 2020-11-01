from typing import List, NamedTuple, Tuple, Optional, Dict

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


class GameState:
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
            known_cards = 0
            for card in self.cards:
                if self.knowledge_tables[card.category][player][card] == Knowledge.TRUE:
                    known_cards += 1
            if known_cards == player.cardAmount:
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
                    if not self.has_solution(self.knowledge_tables):
                        self.knowledge_tables[card.category][player][card] = Knowledge.MAYBE
                        self.add_knowledge(player, card, Knowledge.FALSE)
                        continue

                    self.knowledge_tables[card.category][player][card] = Knowledge.FALSE  # Try to fill in false
                    if not self.has_solution(self.knowledge_tables):
                        self.knowledge_tables[card.category][player][card] = Knowledge.MAYBE
                        self.add_knowledge(player, card, Knowledge.TRUE)
                    else:
                        self.knowledge_tables[card.category][player][card] = Knowledge.MAYBE

    def add_rumour(self, rumour: Rumour) -> None:
        self.rumours.append(rumour)
        for reply in rumour.replies:    # Set all cards to false if rumour is answered false
            player, knowledge = reply
            if knowledge == Knowledge.FALSE:
                self.add_knowledge(player, rumour.weapon, knowledge)
                self.add_knowledge(player, rumour.room, knowledge)
                self.add_knowledge(player, rumour.suspect, knowledge)

    def has_solution(self, brute_knowledge_tables: KnowledgeTables) -> bool:
        # Brute forces knowledge tables and checks the solution with the rumours, edits tables upon findings
        next_maybe = self.find_maybe()
        if next_maybe is None:  # Check the final solution
            return self.check_knowledge(brute_knowledge_tables)

        category, player, card = next_maybe
        brute_knowledge_tables[category][player][card] = Knowledge.TRUE  # Try true
        if self.check_knowledge(brute_knowledge_tables):
            if self.has_solution(brute_knowledge_tables):
                brute_knowledge_tables[category][player][card] = Knowledge.MAYBE  # Reset
                return True

        brute_knowledge_tables[category][player][card] = Knowledge.FALSE   # Try false
        if self.check_knowledge(brute_knowledge_tables):
            if self.has_solution(brute_knowledge_tables):
                brute_knowledge_tables[category][player][card] = Knowledge.MAYBE  # Reset
                return True
        brute_knowledge_tables[category][player][card] = Knowledge.MAYBE  # Reset
        return False

    def check_knowledge(self, test_tables: KnowledgeTables) -> bool:
        # Checks whether given knowledge tables might comply with given rumours
        # Checks whether maximum number of cards is not exceeded

        for rumour in self.rumours:
            rumour_cards = rumour.get_cards()
            for replier, knowledge in rumour.replies:
                if knowledge == Knowledge.FALSE:
                    # Replier should not have any of the rumoured cards
                    for rumour_card in rumour_cards:
                        if test_tables[rumour_card.category][replier][rumour_card] == Knowledge.TRUE:
                            return False
                else:
                    # Replier should have any of the rumoured cards
                    true_or_maybe_found = False
                    for rumour_card in rumour_cards:
                        if test_tables[rumour_card.category][replier][rumour_card] != Knowledge.FALSE:
                            true_or_maybe_found = True
                            break
                    if not true_or_maybe_found:
                        return False

        for player in self.players:
            card_amount = 0
            for card in self.cards:
                if test_tables[card.category][player][card] == Knowledge.TRUE:
                    card_amount += 1
            if card_amount > player.cardAmount:
                return False
        return True

    def find_maybe(self) -> Optional[Tuple[Category, Player, Card]]:
        for player in self.players:
            for card in self.cards:
                if self.knowledge_tables[card.category][player][card] == Knowledge.MAYBE:
                    return card.category, player, card
        return None
