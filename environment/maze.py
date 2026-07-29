from pathlib import Path


class Maze:
    WALL = "#"
    OPEN = "."
    START = "S"
    GOAL = "G"

    def __init__(self, file_path: str):
        self.grid = self._load_maze(file_path)

        self.rows = len(self.grid)
        self.columns = len(self.grid[0])

        self.start_position = self._find_symbol(self.START)
        self.goal_position = self._find_symbol(self.GOAL)

    def _load_maze(self, file_path: str) -> list[list[str]]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Maze file not found: {file_path}")

        with path.open("r", encoding="utf-8") as file:
            lines = [line.rstrip("\n") for line in file if line.strip()]

        if not lines:
            raise ValueError("Maze file is empty.")

        width = len(lines[0])

        if any(len(line) != width for line in lines):
            raise ValueError("Every maze row must have the same length.")

        return [list(line) for line in lines]

    def _find_symbol(self, symbol: str) -> tuple[int, int]:
        for row_index, row in enumerate(self.grid):
            for column_index, cell in enumerate(row):
                if cell == symbol:
                    return row_index, column_index

        raise ValueError(f"Maze does not contain required symbol: {symbol}")

    def is_inside(self, position: tuple[int, int]) -> bool:
        row, column = position

        return (
            0 <= row < self.rows
            and 0 <= column < self.columns
        )

    def is_wall(self, position: tuple[int, int]) -> bool:
        if not self.is_inside(position):
            return True

        row, column = position
        return self.grid[row][column] == self.WALL

    def is_valid_move(self, position: tuple[int, int]) -> bool:
        return self.is_inside(position) and not self.is_wall(position)

    def display(self, robot_position: tuple[int, int] | None = None) -> None:
        for row_index, row in enumerate(self.grid):
            display_row = ""

            for column_index, cell in enumerate(row):
                if robot_position == (row_index, column_index):
                    display_row += "R"
                else:
                    display_row += cell

            print(display_row)