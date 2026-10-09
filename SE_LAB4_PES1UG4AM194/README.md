# Scenario 13 --- Minesweeper

A modular, terminal-based Minesweeper game written in Python for SE Lab
4.

## Objective

Understand and debug a Minesweeper implementation, correct boundary
traversal, implement reliable flag and win behaviour, add difficulty
modes, and provide feedback for player actions.

## Project structure

``` text
13_minesweeper/
├── README.md
├── requirements.txt
├── main.py
├── game.py
├── board.py
├── before.mp4        # Gameplay before the fix (submission evidence)
└── after.mp4         # Gameplay after the fix (submission evidence)
```

The video files are submission evidence and do not need to be present
for the game to run.

## Requirements

-   Python 3.9 or newer
-   No third-party packages required

## How to run

Open a terminal in the project folder and run:

``` bash
python main.py
```

Choose a difficulty when prompted:

  Choice   Difficulty     Board size   Mines
  -------- ------------ ------------ -------
  `1`      Easy                5 × 5       4
  `2`      Medium              6 × 6       6
  `3`      Hard                9 × 9      15

You can also enter `easy`, `medium`, or `hard`.

## Game commands

Enter one command at a time at the `>` prompt.

  -----------------------------------------------------------------------
  Command                             Description
  ----------------------------------- -----------------------------------
  `r row col`                         Reveal the cell at the specified
                                      row and column

  `f row col`                         Place a flag on a hidden cell, or
                                      remove an existing flag

  `q`                                 Quit the game
  -----------------------------------------------------------------------

Examples:

``` text
r 3 4
f 2 2
f 2 2
q
```

Rows and columns are numbered starting at 1. For example, `r 3 4`
reveals row 3, column 4. Do not enter coordinates as `3.4` or `3|4`; use
the command format shown above.

## Board symbols

  Symbol           Meaning
  ---------------- -------------------------------------------------
  `#`              Hidden cell
  `F`              Flagged cell
  `0`              Revealed cell with no adjacent mines
  `1`, `2`, etc.   Number of mines in the surrounding eight cells
  `*`              Mine, shown when the game ends after a mine hit

When a cell with zero adjacent mines is revealed, the game automatically
expands the reveal through neighbouring safe cells.

## Modules

### `main.py`

The application entry point. Creates a `Minesweeper` instance and starts
the game.

### `game.py`

Handles difficulty selection, command parsing, board display, player
feedback, and game termination.

### `board.py`

Stores the board state and implements mine placement, bounds checking,
neighbour traversal, adjacent-mine counting, flood-fill reveal, flag
toggling, and win detection.

### `requirements.txt`

Documents that the project uses only Python's standard library; no
package installation is needed.

## Bugs addressed and features implemented

1.  **Boundary traversal:** Neighbour coordinates are checked using
    `0 <= row < rows` and `0 <= col < cols`. This prevents invalid
    coordinates at board edges and corners.
2.  **Board validation:** Dimensions and mine counts are validated when
    a board is created.
3.  **Flood-fill reveal:** Zero-adjacent regions expand while revealed
    and flagged cells are skipped.
4.  **Flag behaviour:** Flags can be placed and removed on hidden cells.
    Revealed cells cannot be flagged, and flagged cells cannot be
    revealed until unflagged.
5.  **Win detection:** The player wins when all non-mine cells have been
    revealed and no mine has been revealed.
6.  **Difficulty selection:** Easy, Medium, and Hard modes use different
    board sizes and mine counts, with all state kept in memory.
7.  **Input validation:** Invalid commands, non-numeric coordinates, and
    out-of-range coordinates receive clear feedback.
8.  **Action-level feedback:** Feedback is printed for the player's
    command rather than for every internal flood-fill iteration.

## Testing

The lab requires testing the following cases:

-   Neighbour traversal at corners, edges, and centre cells
-   Zero-adjacent flood-fill expansion
-   Mine hits and game-over behaviour
-   Repeated reveals
-   Flag placement and removal
-   Attempting to reveal a flagged cell
-   Invalid coordinates and malformed commands
-   Easy, Medium, and Hard difficulty modes
-   Winning after revealing every safe cell

### Boundary test

Run this small check from the project directory:

``` bash
python -c "from board import Board; b=Board(3,3,0); print(len(list(b.neighbors(0,0))), len(list(b.neighbors(1,1))))"
```

Expected output:

``` text
3 8
```

This confirms that a corner has three neighbours and the centre has
eight. Run the full gameplay tests as well before submitting.

## Submission checklist

-   [ ] Reproduce and document the original boundary bug.
-   [ ] Verify the corrected implementation with boundary and
    invalid-input tests.
-   [ ] Test all three difficulty modes, flags, mine hits, and a
    complete win.
-   [ ] Include a 10-second video showing gameplay before the fix
    (`before.mp4`).
-   [ ] Include a 10-second video showing the fix and new features
    (`after.mp4`).
-   [ ] Include the share link to the complete ChatGPT/LLM conversation.

**Chat/LLM conversation link:** Replace this line with your actual share
link before submission.

## Notes

-   No CSV, JSON, SQLite, or other persistent storage is used.
-   No third-party dependencies are required.
-   Keep the code modular and be prepared to explain how `neighbors()`,
    `adjacent_mines()`, and `reveal()` work together.
