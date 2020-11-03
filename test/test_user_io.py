import unittest

from card import Cards
from knowledge import Knowledge
from load_game_state import load_game_state
from user_io import Table
from watson import Watson


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
        gs = load_game_state('test/game_config.json')
        watson = Watson(gs)
        watson.add_knowledge(gs.players[0], Cards.KNUPPEL, Knowledge.TRUE)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
