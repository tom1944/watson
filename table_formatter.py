class TableFormatter:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self._t = [['' for _ in range(cols)] for _ in range(rows)]

    def get(self, row: int, col: int) -> str:
        return self._t[row][col]

    def set(self, row: int, col: int, s: str):
        self._t[row][col] = s

    def to_string(self) -> str:
        first_col_length = max(len(self.get(row, 0)) for row in range(self.rows))
        other_col_length = max(len(self.get(row, col)) for col in range(1, self.cols) for row in range(self.rows))

        row_strings = []
        for row in range(self.rows):
            row_cells = []
            for col in range(self.cols):
                if col == 0:
                    s = ('{:>' + str(first_col_length) + '}').format(self.get(row, col)[:first_col_length])
                else:
                    s = ('{:^' + str(other_col_length) + '}').format(self.get(row, col)[:other_col_length])
                row_cells.append(s)
            row_string = ' '.join(row_cells)
            row_strings.append(row_string)

        return '\n'.join(row_strings)
