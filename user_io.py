from card import Card, allCards, Category
from gamestate import GameState, Rumour
from knowledge import Knowledge
from typing import List, Any, NamedTuple

characterNames = {
                    'geel': "Van Geelen",
                    'paars': "Pimpel",
                    'groen': "Groenewoud",
                    'blauw': "Blaauw van Draet",
                    'rood': "Roodhart",
                    'wit': "De Wit"
                    }


def print_game_state(game_state: GameState):
    for category in Category:
        pass


def print_table(table: List[List[str]]):
    col_length = max(len(s) for col in table[1:] for s in col)

    for i in range(len(table[0])):
        table[0][i] = '{:>16}'.format(table[0][i])

    for col in table[1:]:
        for i in range(len(col)):
            col[i] = ('{:^' + str(col_length) + '}').format(col[i])

    for row in range(len(table[0])):
        for col in range(len(table)):
            plop(table[col][row] + ' ')
        print('')


def plop(s):
    print(s, end='')


def get_info() -> Rumour:
    input('give input:')


def match_card(card_name: str) -> Card:
    for card in allCards:
        if card_name == card.name:
            return card
    raise Exception(f'card {card_name} not found')