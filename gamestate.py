from typing import List, NamedTuple, Tuple, Optional

from knowledge import Knowledge
from player import Player
from card import Card
from card import Category


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

    def add_card(self, player: Player, card: Card, knowledge: Knowledge):
        category_table = self.knowledge_tables[card.category]

        if category_table[player][card] != Knowledge.MAYBE:   # Check if knowledge is new
            category_table[player][card] = knowledge

            # Exclusion: Other players cannot have the same card
            if knowledge == Knowledge.TRUE:           # Exclude other players if a player has a card
                for other_player in self.players:
                    if other_player != player:
                        category_table[other_player][card] = Knowledge.FALSE

            # Max cards: A player cannot have more cards than he has
            known_cards = 0
            for category in Category:   # Count known cards
                known_cards = known_cards + sum(value == Knowledge.TRUE
                                                for value in self.knowledge_tables[category][player].values())

            # Set all cards that a player does not have to FALSE
            if known_cards == player.cardAmount:
                for card in self.cards:
                    if self.knowledge_tables[card.category][player][card] == Knowledge.MAYBE:
                        self.add_card(player, card, Knowledge.FALSE)

            # Brute force the knowledge table on the rumours
            for category in Category:
                for player in self.players:
                    for card in self.cards:
                        if self.knowledge_tables[category][player][card] == Knowledge.MAYBE:

                            self.knowledge_tables[category][player][card] = Knowledge.TRUE  # Try to fill in true
                            if not self.has_solution(self.knowledge_tables[category][player][card]):
                                self.add_card(player, card, Knowledge.FALSE)
                                continue

                            self.knowledge_tables[category][player][card] = Knowledge.FALSE  # Try to fill in false
                            if not self.has_solution(self.knowledge_tables[category][player][card]):
                                self.add_card(player, card, Knowledge.TRUE)
                            else:
                                self.knowledge_tables[category][player][card] = Knowledge.MAYBE


        else:
            raise Exception(f'Contradiction in table {card.category} player {player.name} card {card.name}')

    def add_rumour(self, rumour):
        self.rumours.append(rumour)
        for reply in rumour.replies:    # Set all cards to false if rumour is answered false
            player, knowledge = reply
            if knowledge == knowledge.FALSE:
                self.add_card(player, rumour.weapon, knowledge)
                self.add_card(player, rumour.room, knowledge)
                self.add_card(player, rumour.suspect, knowledge)

    def has_solution(self, brute_knowledge_tables) -> bool:
        # Brute forces knowledge tables and checks the solution with the rumours, edits tables upon findings
        next_maybe = self.find_next_maybe()
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

    def check_knowledge(self, test_tables):
        # Checks whether given knowledge tables might comply with given rumours
        # NOTE: Only checks replies that debunked the rumours, as negative replies are written to knowledge right away

        for rumour in self.rumours:
            weapon = rumour.weapon
            room = rumour.room
            suspect = rumour.suspect
            responder = [reply for reply in rumour.replies if Knowledge.TRUE in reply]
            if test_tables[weapon.category][responder][weapon] == Knowledge.FALSE\
                    and test_tables[room.category][responder][room] == Knowledge.FALSE\
                    and test_tables[suspect.category][responder][suspect] == Knowledge.FALSE:
                return False
        return True

    def find_next_maybe(self) -> Optional[Tuple[Category, Player, Card]]:
        for cat in Category:
            for player in self.players:
                for card in self.cards:
                    if self.knowledge_tables[cat][player][card] == Knowledge.MAYBE:
                        return cat, player, card
        return None
