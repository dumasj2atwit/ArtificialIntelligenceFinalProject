from environment.maze import Maze
from environment.robot import Robot, Action


class MazeEnvironment:

    def __init__(self, maze_file):
        self.maze = Maze(maze_file)
        self.robot = Robot(self.maze)

        # Cells the robot has discovered so far.
        # Key = (row, column)
        # Value = maze symbol (#, ., S, G)
        self.discovered = {}

    def reset(self):
        self.robot.reset()

        self.discovered = {}

        # Robot can see its starting position and adjacent cells.
        self.update_discovered()

        return self.robot.position

    def step(self, action):
        moved = self.robot.move(action)

        reward = 0
        done = False

        if not moved:
            reward = -5

        else:
            # Moving to a new position reveals nearby cells.
            self.update_discovered()

            if self.robot.reached_goal():
                reward = 100
                done = True
            else:
                reward = -1

        return self.robot.position, reward, done

    def get_visible_cells(self):
        row, column = self.robot.position

        positions = [
            (row, column),
            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1),
        ]

        visible = {}

        for position in positions:
            if self.maze.is_inside(position):
                r, c = position
                visible[position] = self.maze.grid[r][c]

        return visible

    def update_discovered(self):
        visible = self.get_visible_cells()

        for position, cell in visible.items():
            self.discovered[position] = cell

    def goal_discovered(self):
        return self.maze.goal_position in self.discovered

    def render(self):
        self.maze.display(self.robot.position)