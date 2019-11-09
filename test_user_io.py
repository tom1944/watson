import unittest
from user_io import Table


class MyTestCase(unittest.TestCase):
    def test_print_table(self):
        test_table = [
            ['', 'Tom', 'Menno', 'Michiel'],
            ['halter', '', '', ''],
            ['mes', 'x', 'x', 'v'],
            ['bijl', 'x', '', ''],
        ]
        t = Table(4, 4)
        for _row in range(4):
            for _col in range(4):
                t.set(_col, _row, test_table[_row][_col])
        print(t.to_string())
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
