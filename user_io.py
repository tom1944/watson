from card import Card, Category
from gamestate import GameState
from table_formatter import TableFormatter
from watson import Player
from knowledge import Knowledge
from typing import List, Dict


def game_state_to_string(game_state: GameState) -> str:
    k_table: Dict[Player, Dict[Card, Knowledge]] = {}

    for player in game_state.players:
        column: Dict[Card, Knowledge] = {}
        for card in game_state.cards:
            column[card] = game_state.knowledge_tables[card.category][player][card]
        k_table[player] = column

    lines = []
    for category in Category:
        cat_cards = [card for card in game_state.cards if card.category == category]
        lines.append(print_category_table(cat_cards, game_state, k_table))
    return "\n".join(lines)


def print_category_table(category_cards, game_state, k_table):
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


def match_input_string_from_set(start: str, input_set: List[str]) -> str:
    while True:
        matches = [i for i in input_set if i.lower().startswith(start.lower())]
        if len(matches) == 0:
            start = input(f'Input "{start}" invalid. Choose one of: {", ".join(matches)}.')
        elif len(matches) == 1:
            return matches[0]
        elif start in matches:
            return start
        else:
            start = input(f'Input "{start}" ambiguous. Did you mean one of: {", ".join(matches)}?')
