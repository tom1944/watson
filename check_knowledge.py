from typing import List, Dict

from card import Card
from knowledge import Knowledge
from knowledge_table import KnowledgeTable
from player import Player
from session import Session


# assumes new_player_hands only contains free cards
def check_knowledge(knowledge_table: KnowledgeTable, session: Session,
                    new_player_hands: Dict[Player, List[Card]] = None) -> bool:

    player_hands, murder_cards, free_cards = knowledge_table.current_player_hands()

    players = session.context.players
    for player in players:
        if new_player_hands is not None:
            player_hands[player] += new_player_hands[player]
            for card in new_player_hands[player]:
                if card in free_cards:
                    free_cards.remove(card)
        if len(player_hands[player]) > player.cardAmount:
            return False

    for rumour in session.rumours:
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
