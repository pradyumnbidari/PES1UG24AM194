
import random

DEFAULT_ROWS = 6
DEFAULT_COLS = 6
DEFAULT_MINES = 6


class Board:
    def __init__(
        self,
        rows=DEFAULT_ROWS,
        cols=DEFAULT_COLS,
        mines=DEFAULT_MINES,
    ):
        if (
            not isinstance(rows, int)
            or isinstance(rows, bool)
            or not isinstance(cols, int)
            or isinstance(cols, bool)
            or rows <= 0
            or cols <= 0
        ):
            raise ValueError(
                "Rows and columns must be positive integers."
            )

        if (
            not isinstance(mines, int)
            or isinstance(mines, bool)
            or mines < 0
            or mines >= rows * cols
        ):
            raise ValueError(
                "Mines must be non-negative and fewer than board cells."
            )

        self.rows = rows
        self.cols = cols
        self.mine_total = mines

        self.mines = self._build_mines()
        self.revealed = set()
        self.flags = set()

    def _build_mines(self):
        cells = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
        ]

        return set(random.sample(cells, self.mine_total))

    def in_bounds(self, r, c):
        return (
            0 <= r < self.rows
            and 0 <= c < self.cols
        )

    def neighbors(self, r, c):
        if not self.in_bounds(r, c):
            return

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue

                nr = r + dr
                nc = c + dc

                if self.in_bounds(nr, nc):
                    yield nr, nc

    def adjacent_mines(self, r, c):
        if not self.in_bounds(r, c):
            raise ValueError("Cell is outside the board.")

        return sum(
            neighbor in self.mines
            for neighbor in self.neighbors(r, c)
        )

    def reveal(self, start):
        r, c = start

        if not self.in_bounds(r, c):
            return False

        if start in self.revealed or start in self.flags:
            return False

        stack = [start]
        hit_mine = False

        while stack:
            pos = stack.pop()

            if pos in self.revealed or pos in self.flags:
                continue

            self.revealed.add(pos)

            r, c = pos

            if pos in self.mines:
                hit_mine = True
                continue

            if self.adjacent_mines(r, c) == 0:
                for neighbor in self.neighbors(r, c):
                    if (
                        neighbor not in self.revealed
                        and neighbor not in self.flags
                    ):
                        stack.append(neighbor)

        return hit_mine

    def toggle_flag(self, pos):
        r, c = pos

        if not self.in_bounds(r, c):
            return False

        if pos in self.revealed:
            return False

        if pos in self.flags:
            self.flags.remove(pos)
        else:
            self.flags.add(pos)

        return True

    def won(self):
        for r in range(self.rows):
            for c in range(self.cols):
                pos = (r, c)

                if pos not in self.mines and pos not in self.revealed:
                    return False

        return self.revealed.isdisjoint(self.mines)
