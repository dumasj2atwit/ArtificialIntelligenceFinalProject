import pygame

from environment.maze import Maze
from environment.robot import Robot


class PyGameRenderer:
    CELL_SIZE = 24

    def __init__(self, maze: Maze, robot: Robot):
        self.maze = maze
        self.robot = robot

        self.width = maze.columns * self.CELL_SIZE
        self.height = maze.rows * self.CELL_SIZE

        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Robot")

        self.clock = pygame.time.Clock()

        # Draw the first frame so a window appears immediately, but all
        # per-frame drawing now lives in render() so it can be called
        # repeatedly as the robot moves.
        self.render(self.robot)

    def process_events(self) -> bool:
        """Pump the pygame event queue. Returns False if the user closed
        the window, so callers know to stop their run loop."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        return True

    def render(self, robot: Robot):
        self.robot = robot

        self.screen.fill((255, 255, 255))

        for row in range(self.maze.rows):
            for column in range(self.maze.columns):

                cell = self.maze.grid[row][column]

                x = column * self.CELL_SIZE
                y = row * self.CELL_SIZE

                rectangle = pygame.Rect(
                    x,
                    y,
                    self.CELL_SIZE,
                    self.CELL_SIZE,
                )

                # Walls
                if cell == Maze.WALL:
                    pygame.draw.rect(
                        self.screen,
                        (40, 40, 40),
                        rectangle,
                    )

                # Open cells
                else:
                    pygame.draw.rect(
                        self.screen,
                        (230, 230, 230),
                        rectangle,
                    )

                # Grid
                pygame.draw.rect(
                    self.screen,
                    (180, 180, 180),
                    rectangle,
                    1,
                )

        self._draw_start()
        self._draw_goal()
        self._draw_visited()
        self._draw_robot()

        pygame.display.flip()
        self.clock.tick(60)

    def _draw_start(self):
        row, column = self.maze.start_position

        pygame.draw.rect(
            self.screen,
            (100, 180, 100),
            self._cell_rectangle(row, column),
        )

    def _draw_goal(self):
        row, column = self.maze.goal_position

        pygame.draw.rect(
            self.screen,
            (220, 100, 100),
            self._cell_rectangle(row, column),
        )

    def _draw_visited(self):
        for row, column in self.robot.visited_positions:

            # Don't cover the start or goal.
            if (
                (row, column) == self.maze.start_position
                or (row, column) == self.maze.goal_position
            ):
                continue

            pygame.draw.rect(
                self.screen,
                (190, 210, 230),
                self._cell_rectangle(row, column),
            )

    def _draw_robot(self):
        row, column = self.robot.position

        rectangle = self._cell_rectangle(row, column)
        center = rectangle.center

        pygame.draw.circle(
            self.screen,
            (50, 100, 220),
            center,
            self.CELL_SIZE // 3,
        )

    def _cell_rectangle(
        self,
        row: int,
        column: int,
    ) -> pygame.Rect:

        return pygame.Rect(
            column * self.CELL_SIZE,
            row * self.CELL_SIZE,
            self.CELL_SIZE,
            self.CELL_SIZE,
        )

    def close(self):
        pygame.quit()