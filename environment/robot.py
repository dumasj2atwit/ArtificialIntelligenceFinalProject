from enum import Enum

from environment.maze import Maze


class Action(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


class Robot:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.position = maze.start_position
        self.visited_positions = {self.position}
        self.steps = 0

    def reset(self) -> None:
        self.position = self.maze.start_position
        self.visited_positions = {self.position}
        self.steps = 0

    def get_next_position(self, action: Action) -> tuple[int, int]:
        row_change, column_change = action.value
        row, column = self.position

        return row + row_change, column + column_change

    def move(self, action: Action) -> bool:
        next_position = self.get_next_position(action)

        if not self.maze.is_valid_move(next_position):
            return False

        self.position = next_position
        self.visited_positions.add(self.position)
        self.steps += 1

        return True

    def reached_goal(self) -> bool:
        return self.position == self.maze.goal_position