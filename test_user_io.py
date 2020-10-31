import unittest

from card import Cards
from gameconfig import load_game_config
from gamestate import GameState
from knowledge import Knowledge
from user_io import Table


def init_game_state():
    test_game_config = load_game_config()
    return GameState(test_game_config.players, test_game_config.used_cards)


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
        gs.add_knowledge(gs.players[0], Cards.KNUPPEL, Knowledge.TRUE)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
