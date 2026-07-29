from environment.maze import Maze
from environment.robot import Robot, Action

class MazeEnvironment:

    def __init__(self, maze_file):
        self.maze = Maze(maze_file)
        self.robot = Robot(self.maze)
    def reset(self):
        self.robot.reset()
        return self.robot.position
    def step(self, action):

        moved = self.robot.move(action)

        reward = 0

        done = False

        if not moved:
            reward = -5

        elif self.robot.reached_goal():
            reward = 100
            done = True

        else:
            reward = -1

        return self.robot.position, reward, done
    def render(self):
        self.maze.display(self.robot.position)