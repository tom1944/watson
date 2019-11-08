from card import Card, allCards
from gamestate import GameState, Rumour
from knowledge import Knowledge

characterNames = {
                    'geel': "Van Geelen",
                    'paars': "Pimpel",
                    'groen': "Groenewoud",
                    'blauw': "Blaauw van Draet",
                    'rood': "Roodhart",
                    'wit': "De Wit"
                    }


def print_gamestate(game_state: GameState):
    pass


def get_info() -> Rumour:
    pass


def match_card(card_name: str) -> Card:
    for card in allCards:
        if card_name == card.name:
            return card
    raise Exception(f'card {card_name} not found')