import unittest

from card import allCards
from gameconfig import loadGameConfig
from gamestate import GameState
from knowledge import Knowledge
from user_io import Table, match_card


def init_game_state():
    players, open_cards, your_cards = loadGameConfig()

    used_cards = [c for c in allCards if c not in open_cards]
    return GameState(players, used_cards)


class MyTestCase(unittest.TestCase):

    def test_print_table(self):
        test_table = [
            ['', 'Tom', 'Menno', 'Michiel'],
            ['Halter', '', '', ''],
            ['Mes', 'x', 'x', 'v'],
            ['Bijl', 'x', '', ''],
        ]
        t = Table(4, 4)
        for _row in range(4):
            for _col in range(4):
                t.set(_col, _row, test_table[_row][_col])
        print(t.to_string())
        self.assertTrue(True)

    def test_print_game_state(self):
        gs = init_game_state()
        gs.add_card(gs.players[0], match_card('Knuppel'), Knowledge.TRUE)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
