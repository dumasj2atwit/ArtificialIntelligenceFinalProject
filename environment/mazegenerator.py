import random
from pathlib import Path


def generate_maze(rows: int, cols: int) -> list[list[str]]:
    # Recursive-backtracking maze generation works best with odd dimensions.
    if rows % 2 == 0:
        rows += 1

    if cols % 2 == 0:
        cols += 1

    maze = [["#" for _ in range(cols)] for _ in range(rows)]

    start = (1, 1)
    maze[1][1] = "."

    stack = [start]

    directions = [
        (-2, 0),
        (2, 0),
        (0, -2),
        (0, 2),
    ]

    while stack:
        row, col = stack[-1]

        unvisited_neighbors = []

        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc

            if (
                1 <= new_row < rows - 1
                and 1 <= new_col < cols - 1
                and maze[new_row][new_col] == "#"
            ):
                unvisited_neighbors.append(
                    (new_row, new_col, dr, dc)
                )

        if unvisited_neighbors:
            new_row, new_col, dr, dc = random.choice(
                unvisited_neighbors
            )

            # Carve through the wall between the two cells.
            wall_row = row + dr // 2
            wall_col = col + dc // 2

            maze[wall_row][wall_col] = "."
            maze[new_row][new_col] = "."

            stack.append((new_row, new_col))

        else:
            stack.pop()

    # Start is always top-left interior cell.
    maze[1][1] = "S"

    # Goal is placed at the opposite interior corner.
    maze[rows - 2][cols - 2] = "G"

    return maze


def save_maze(
    maze: list[list[str]],
    filename: str,
) -> None:
    path = Path(filename)

    # Make the folder if it does not exist.
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        for row in maze:
            file.write("".join(row) + "\n")


def generate_difficulty_maze(difficulty: str) -> None:
    sizes = {
        "easy": (11, 11),
        "medium": (21, 21),
        "hard": (31, 31),
    }

    if difficulty not in sizes:
        raise ValueError(
            "Difficulty must be easy, medium, or hard."
        )

    rows, cols = sizes[difficulty]

    maze = generate_maze(rows, cols)

    save_maze(
        maze,
        f"mazes/{difficulty}.txt",
    )


if __name__ == "__main__":
    generate_difficulty_maze("easy")
    generate_difficulty_maze("medium")
    generate_difficulty_maze("hard")

    print("Generated easy, medium, and hard mazes.")