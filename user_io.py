from cmd import Cmd

from card import Card, Category
from gamestate import GameState
from table_formatter import TableFormatter
from watson import Player, Watson
from knowledge import Knowledge
from typing import List, Dict, Optional


class WatsonShell(Cmd):
    def __init__(self, watson: Watson, **kwargs):
        Cmd.__init__(self, kwargs)
        self.watson = watson
        self.intro = "Welcome to Watson, the Cluedo assistent.   Type help or ? to list commands.\n"
        self.prompt = ">>> "

    def do_card(self, arg):
        """"card <card> <owner>"""
        args = arg.split()

        if len(args) != 2:
            print('Usage: ' + str(self.do_card.__doc__))
            return False

        card_name, owner_name = args

        card = match_card(card_name, self.watson.game_state.used_cards)
        owner = match_player(owner_name, self.watson.game_state.players)

        if not card or not owner:
            return False

        self.watson.add_knowledge(owner, card, Knowledge.TRUE)

    def do_c(self, arg):
        """"Alias for card"""
        self.do_card(arg)

    def do_rumour(self, arg):
        """"rumour <claimer> <card1> <card2> <card3>"""
        pass

    def do_r(self, arg):
        """Alias for rumour"""
        self.do_rumour(arg)


def knowledge_table_to_string(watson: Watson) -> str:
    k_table: Dict[Player, Dict[Card, Knowledge]] = {}

    for player in watson.game_state.players:
        column: Dict[Card, Knowledge] = {}
        for card in watson.game_state.used_cards:
            column[card] = watson.knowledge_tables[card.category][player][card]
        k_table[player] = column

    lines = []
    for category in Category:
        cat_cards = [card for card in watson.game_state.cards if card.category == category]
        lines.append(print_category_table(cat_cards, watson.game_state, k_table))
    return "\n".join(lines)


def print_category_table(category_cards: List[Card], game_state: GameState, k_table):
    players = game_state.players
    category_cards.sort(key=lambda card: card.name)

    table = TableFormatter(len(players) + 1, len(category_cards) + 1)
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


def match_player(start_of_player_name: str, players: List[Player]) -> Player:
    player_name = match_input_string_from_set(start_of_player_name, [p.name for p in players])
    return [p for p in players if p.name == player_name][0]


def match_card(start_of_card_name: str, cards: List[Card]) -> Card:
    card_name = match_input_string_from_set(start_of_card_name, [c.name for c in cards])
    return [c for c in cards if c.name == card_name][0]


def match_input_string_from_set(start: str, input_set: List[str]) -> Optional[str]:
    matches = [i for i in input_set if i.lower().startswith(start.lower())]
    if len(matches) == 0:
        print(f'Input "{start}" invalid. Choose one of: {", ".join(matches)}.')
        return None
    elif len(matches) == 1:
        return matches[0]
    elif start in matches:
        return start
    else:
        print(f'Input "{start}" ambiguous. Did you mean one of: {", ".join(matches)}?')
        return None
