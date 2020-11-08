class TableFormatter:
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