from typing import List, Dict

from source.data.card import Card
from source.data.knowledge import Knowledge
from source.data.knowledge_table import KnowledgeTable
from source.data.player import Player
from source.data.clues import Clues


def check_knowledge(knowledge_table: KnowledgeTable, clues: Clues,
                    new_player_hands: Dict[Player, List[Card]] = None) -> bool:

    player_hands, murder_cards, free_cards = knowledge_table.current_player_hands()

    players = clues.context.players
    for player in players:
        if new_player_hands is not None:
            player_hands[player] += new_player_hands[player]
            player_hands[player] = list(set(player_hands[player]))  # To get unique elements from list
            for card in new_player_hands[player]:
                if card in free_cards:
                    free_cards.remove(card)
        if len(player_hands[player]) > player.cardAmount:
            return False

    for rumour in clues.rumours:
        rumour_cards = rumour.rumour_cards
        for replier, knowledge in rumour.replies:
            has_rumour_card = set(rumour_cards).isdisjoint(player_hands[replier])
            if knowledge == Knowledge.FALSE:
                # Replier should not have any of the rumoured cards
                if not has_rumour_card:
                    return False
            elif knowledge == Knowledge.TRUE:
                # Replier should have any of the rumoured cards
                if replier.cardAmount == len(player_hands[replier]) and has_rumour_card:
                    return False
                if set(rumour_cards).isdisjoint(free_cards) and has_rumour_card:
                    return False
    return True
