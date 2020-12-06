from typing import Tuple, List, Dict

from card import Category, Card
from knowledge import Knowledge
from player import Player


class KnowledgeTable:
    def __init__(self, players: List[Player], cards: List[Card]):
        self.players = players
        self.cards = cards
        self._knowledge_tables = {}

        for category in Category:
            table = {}
            for player in players:
                column = {}
                for card in cards:
                    if card.category == category:
                        column[card] = Knowledge.MAYBE
                table[player] = column
            self._knowledge_tables[category] = table

    def get_knowledge(self, player: Player, card: Card) -> Knowledge:
        return self._knowledge_tables[card.category][player][card]

    def set_item(self, player: Player, card: Card, knowledge: Knowledge):
        if self._knowledge_tables[card.category][player][card] != Knowledge.MAYBE:
            if self._knowledge_tables[card.category][player][card] != knowledge:
                raise ValueError(
                    f'Contradiction in table {card.category.value} player {player.name} card {card.name}: '
                    f'Attempt to overwrite {self._knowledge_tables[card.category][player][card]} with {knowledge}'
                )
        self.set_item_without_check(player, card, knowledge)

    def set_item_without_check(self, player: Player, card: Card, knowledge: Knowledge):
        self._knowledge_tables[card.category][player][card] = knowledge

    def get_current_player_hands(self) -> Tuple[Dict[Player, List[Card]], List[Card], List[Card]]:
        player_hands = {p: [] for p in self.players}
        murderer_cards = []
        free_cards = []

        for card in self.cards:
            all_false = True

            for player in self.players:
                knowledge = self.get_knowledge(player, card)
                if knowledge == Knowledge.TRUE:
                    player_hands[player].append(card)
                    all_false = False
                    break
                elif knowledge == Knowledge.MAYBE:
                    free_cards.append(card)
                    all_false = False
                    break

            if all_false:
                murderer_cards.append(card)

        return player_hands, murderer_cards, free_cards
