import unittest

from table_formatter import TableFormatter


class TestTableFormatter(unittest.TestCase):
    def test_table_to_string(self):
        test_table = [
            ['', 'Tom', 'Menno', 'Michiel'],
            ['Halter', '', '', ''],
            ['Mes', 'x', 'x', 'v'],
            ['Bijl', 'x', '', ''],
        ]
        t = TableFormatter(4, 4)
        for _row in range(4):
            for _col in range(4):
                t.set(_row, _col, test_table[_row][_col])

        expected = '\n'.join([
            "         Tom    Menno  Michiel ",
            "Halter                         ",
            "   Mes    x       x       v    ",
            "  Bijl    x                    ",
            "",
        ])

        self.assertEqual(t.to_string(), expected)
