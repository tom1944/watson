from card import Card, allCards, Category
from gamestate import GameState, Rumour, Player
from knowledge import Knowledge
from typing import List, Any, Dict, Callable

characterNames = {
                    'geel': "Van Geelen",
                    'paars': "Pimpel",
                    'groen': "Groenewoud",
                    'blauw': "Blaauw van Draet",
                    'rood': "Roodhart",
                    'wit': "De Wit"
                    }


def print_game_state(game_state: GameState):
    k_table: Dict[Player, Dict[Card, Knowledge]] = {}

    for player in game_state.players:
        column: Dict[Card, Knowledge] = {}
        for card in game_state.cards:
            column[card] = game_state.knowledge_tables[card.category][player][card]
        k_table[player] = column

    for category in Category:
        cat_cards = [card for card in game_state.cards if card.category == category]
        print(print_category_table(cat_cards, game_state, k_table))


def print_category_table(category_cards, game_state, k_table):
    players = game_state.players
    category_cards.sort(key=lambda card: card.name)

    table = Table(len(players) + 1, len(category_cards) + 1)
    # Set the player names in the table
    for p in range(len(players)):
        table.set(p + 1, 0, players[p].name)
    # Set the card names in the table
    for c in range(len(category_cards)):
        table.set(0, c + 1, category_cards[c].name)
    # fill the table
    for card_i in range(len(category_cards)):
        for player_i in range(len(players)):
            card = category_cards[card_i]
            player = players[player_i]
            s = knowledge_to_str(k_table[player][card])
            table.set(player_i + 1, card_i + 1, s)
    return table.to_string()


def knowledge_to_str(knowledge: Knowledge) -> str:
    return {
        Knowledge.TRUE: 'v',
        Knowledge.FALSE: 'x',
        Knowledge.MAYBE: '.',
    }[knowledge]


class Table:
    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self._t = [['' for _ in range(cols)] for _ in range(rows)]

    def get(self, col: int, row: int) -> str:
        return self._t[row][col]

    def set(self, col: int, row: int, s: str):
        self._t[row][col] = s

    def transpose(self):
        t2 = zip(*self._t)
        self._t = list(map(list, t2))

    def to_string(self) -> str:
        first_col_length = max(len(self.get(0, row)) for row in range(self.rows))
        other_col_length = max(len(self.get(col, row)) for col in range(1, self.cols) for row in range(self.rows))

        sb = ''
        for row in range(self.rows):
            for col in range(self.cols):
                if col == 0:
                    s = ('{:>' + str(first_col_length) + '}').format(self.get(col, row)[:first_col_length])
                else:
                    s = ('{:^' + str(other_col_length) + '}').format(self.get(col, row)[:other_col_length])
                sb += s + ' '
            sb += '\n'

        return sb


def get_info(game_state: GameState) -> Rumour:
    rumour = get_rumour_claim(game_state)
    while True:
        if get_input_string_from_set('Is there another reply? ', ['y', 'n'], lambda x: x) == 'n':
            break
        player = get_input_string_from_set('Who gives the reply? ', game_state.players, lambda p: p.name)
        reply = get_input_string_from_set('Does replier show a card? ', ['y', 'n'], lambda x: x) == 'n'
        if reply == 'y':
            knowledge = Knowledge.TRUE
        else:
            knowledge = Knowledge.FALSE
        rumour.replies.append((player, knowledge))
    return rumour


def get_rumour_claim(game_state: GameState) -> Rumour:
    player = get_input_string_from_set('Who is on the turn? ', game_state.players, lambda p: p.name)
    room = get_input_string_from_set('Room? ', [c for c in game_state.cards if c.category == Category.ROOM],
                                     lambda c: c.name)
    suspect = get_input_string_from_set('Suspect? ',
                                        [c for c in game_state.cards if c.category == Category.CHARACTER],
                                        lambda c: c.name)
    weapon = get_input_string_from_set('Weapon? ', [c for c in game_state.cards if c.category == Category.WEAPON],
                                       lambda p: p.name)
    return Rumour(player, weapon, room, suspect, [])


def get_input_string_from_set(msg: str, input_set: List[Any], get_str_function: Callable[[Any], str]) -> Any:
    allowed_input_strings = [get_str_function(i) for i in input_set] + ['exit']
    while True:
        input_string = input(msg)
        if input_string == 'exit':
            raise Exception('exit from input function')  # todo: change this to not use Exceptions for normal control flow
        matches = [i for i in input_set if get_str_function(i) == input_string]
        if len(matches) == 0:
            print('choose one of ', ', '.join(allowed_input_strings))
        elif len(matches) == 1:
            return matches[0]
        else:
            print(f'Input {input_string} ambiguous. Input set: {input_set}')


def match_card(card_name: str) -> Card:
    for card in allCards:
        if card_name == card.name:
            return card
    raise Exception(f'card {card_name} not found')
