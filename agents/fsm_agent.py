from enum import Enum

from environment.environment import MazeEnvironment
from environment.robot import Action


class FSMState(Enum):
    EXPLORE = 1
    BACKTRACK = 2
    FINISHED = 3


class FSMAgent:
    def __init__(self, environment: MazeEnvironment):
        self.environment = environment

        self.state = FSMState.EXPLORE
        self.previous_state = self.state

        self.path_stack: list[tuple[int, int]] = []
        self.visited: set[tuple[int, int]] = set()

        self.dead_ends = 0
        self.backtrack_steps = 0

    def reset(self) -> None:
        start_position = self.environment.reset()

        self.state = FSMState.EXPLORE
        self.previous_state = self.state

        self.path_stack = [start_position]
        self.visited = {start_position}

        self.dead_ends = 0
        self.backtrack_steps = 0

    def choose_action(self) -> Action | None:
        if self.state == FSMState.FINISHED:
            return None

        current_position = self.environment.robot.position

        for action in Action:
            next_position = self.environment.robot.get_next_position(action)

            if (
                self.environment.maze.is_valid_move(next_position)
                and next_position not in self.visited
            ):
                self.previous_state = self.state
                self.state = FSMState.EXPLORE

                self.visited.add(next_position)
                self.path_stack.append(next_position)

                return action

        if self.state != FSMState.BACKTRACK:
            self.dead_ends += 1

        self.previous_state = self.state
        self.state = FSMState.BACKTRACK

        if len(self.path_stack) <= 1:
            return None

        self.path_stack.pop()
        previous_position = self.path_stack[-1]

        self.backtrack_steps += 1

        return self._get_action_to_position(
            current_position,
            previous_position,
        )

    def _get_action_to_position(
        self,
        current_position: tuple[int, int],
        target_position: tuple[int, int],
    ) -> Action:
        current_row, current_column = current_position
        target_row, target_column = target_position

        difference = (
            target_row - current_row,
            target_column - current_column,
        )

        for action in Action:
            if action.value == difference:
                return action

        raise ValueError(
            "Target position is not adjacent to current position."
        )