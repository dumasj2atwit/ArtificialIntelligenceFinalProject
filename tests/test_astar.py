from agents.astar import astar
from environment.maze import Maze


def test_astar_finds_path() -> None:
    maze = Maze("mazes/easy.txt")

    path = astar(
        maze,
        maze.start_position,
        maze.goal_position,
    )

    assert path is not None
    assert path[0] == maze.start_position
    assert path[-1] == maze.goal_position

    for position in path:
        assert maze.is_valid_move(position)