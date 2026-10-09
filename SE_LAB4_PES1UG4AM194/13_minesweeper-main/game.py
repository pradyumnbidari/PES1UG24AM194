
from board import Board


DIFFICULTIES = {
    "easy": (5, 5, 4),
    "medium": (6, 6, 6),
    "hard": (9, 9, 15),
}


class Minesweeper:
    def __init__(self):
        self.board = Board()
        self.difficulty = "medium"

    def display(self, reveal_mines=False):
        board = self.board

        print()
        print("    " + " ".join(
            f"{c + 1:2}" for c in range(board.cols)
        ))

        for r in range(board.rows):
            cells = []

            for c in range(board.cols):
                pos = (r, c)

                if reveal_mines and pos in board.mines:
                    symbol = "*"
                elif pos in board.flags:
                    symbol = "F"
                elif pos not in board.revealed:
                    symbol = "#"
                elif pos in board.mines:
                    symbol = "*"
                else:
                    symbol = str(board.adjacent_mines(r, c))

                cells.append(f"{symbol:2}")

            print(f"{r + 1:2}  " + " ".join(cells))

        print()

    def choose_difficulty(self):
        print("\nChoose difficulty:")
        print("1. Easy   - 5 x 5, 4 mines")
        print("2. Medium - 6 x 6, 6 mines")
        print("3. Hard   - 9 x 9, 15 mines")

        choices = {
            "1": "easy",
            "2": "medium",
            "3": "hard",
            "easy": "easy",
            "medium": "medium",
            "hard": "hard",
        }

        while True:
            choice = input("Enter 1, 2, or 3: ").strip().lower()

            if choice in choices:
                difficulty = choices[choice]
                rows, cols, mines = DIFFICULTIES[difficulty]

                self.board = Board(rows, cols, mines)
                self.difficulty = difficulty

                print(
                    f"\n{difficulty.title()} mode selected: "
                    f"{rows} rows, {cols} columns, {mines} mines."
                )
                return

            print("Invalid choice. Please enter 1, 2, or 3.")

    def run(self):
        print("\n========== MINESWEEPER ==========")

        self.choose_difficulty()

        print("\nCommands:")
        print("r row col  - Reveal a cell")
        print("f row col  - Place or remove a flag")
        print("q          - Quit the game")
        print("Example: r 3 4")

        while True:
            self.display()

            command = input("> ").strip().lower()

            if command == "q":
                print("Game ended. Thanks for playing!")
                return

            parts = command.split()

            if len(parts) != 3 or parts[0] not in ("r", "f"):
                print("Invalid command. Use r row col, f row col, or q.")
                continue

            action = parts[0]

            try:
                row = int(parts[1])
                col = int(parts[2])
            except ValueError:
                print("Row and column must be numbers.")
                continue

            r = row - 1
            c = col - 1
            pos = (r, c)

            if not self.board.in_bounds(r, c):
                print(
                    f"Invalid coordinates. Enter row 1-{self.board.rows} "
                    f"and column 1-{self.board.cols}."
                )
                continue

            if action == "f":
                if not self.board.toggle_flag(pos):
                    print("Cannot flag a revealed cell.")
                elif pos in self.board.flags:
                    print(f"Flag placed at row {row}, column {col}.")
                else:
                    print(f"Flag removed from row {row}, column {col}.")

                continue

            if pos in self.board.flags:
                print("This cell is flagged. Remove the flag first.")
                continue

            if pos in self.board.revealed:
                print("This cell is already revealed.")
                continue

            hit_mine = self.board.reveal(pos)

            if hit_mine:
                self.display(reveal_mines=True)
                print("BOOM! You hit a mine. Game over!")
                return

            print(f"Cell ({row}, {col}) revealed.")

            if self.board.won():
                self.display()
                print("CONGRATULATIONS! You cleared every safe cell!")
                print("YOU WIN!")
                return
