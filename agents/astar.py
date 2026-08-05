import heapq

from environment.maze import Maze


Position = tuple[int, int]


def heuristic(position: Position, goal: Position) -> int:
    row, column = position
    goal_row, goal_column = goal

    return abs(row - goal_row) + abs(column - goal_column)


def get_neighbors(
    maze: Maze,
    position: Position,
) -> list[Position]:
    row, column = position

    possible_neighbors = [
        (row - 1, column),
        (row, column + 1),
        (row + 1, column),
        (row, column - 1),
    ]

    return [
        neighbor
        for neighbor in possible_neighbors
        if maze.is_valid_move(neighbor)
    ]


def reconstruct_path(
    came_from: dict[Position, Position],
    current: Position,
) -> list[Position]:
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path


def astar(
    maze: Maze,
    start: Position,
    goal: Position,
) -> list[Position] | None:
    open_set: list[tuple[int, Position]] = []
    heapq.heappush(open_set, (0, start))

    came_from: dict[Position, Position] = {}

    g_score: dict[Position, float] = {
        start: 0
    }

    f_score: dict[Position, float] = {
        start: heuristic(start, goal)
    }

    visited: set[Position] = set()

    while open_set:
        _, current = heapq.heappop(open_set)

        if current in visited:
            continue

        if current == goal:
            return reconstruct_path(came_from, current)

        visited.add(current)

        for neighbor in get_neighbors(maze, current):
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score

                new_f_score = tentative_g_score + heuristic(
                    neighbor,
                    goal,
                )

                f_score[neighbor] = new_f_score

                heapq.heappush(
                    open_set,
                    (new_f_score, neighbor),
                )

    return None