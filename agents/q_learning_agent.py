import random
from collections import defaultdict

from environment.environment import MazeEnvironment
from environment.robot import Action


class QLearningAgent:

    def __init__(
        self,
        enviorment: MazeEnvironment,
        learning_rate: float = 0.2,
        discount_factor: float = 0.9,
        exploration_rate: float = 0.1,
    ):

        self.enviorment = enviorment
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate

        self.q_values = defaultdict(float)

    def get_state(self) -> tuple:
        position = self.enviorment.robot.position

        local_obs = []

        for action in Action:
            next_position = self.enviorment.robot.get_next_position(action)

            is_wall = not self.enviorment.maze.is_valid_move(next_position)

            is_visted = next_position in self.enviorment.robot.visited_positions

            local_obs.append((is_wall, is_visted))

        return (position, tuple(local_obs))

    def get_Q_value(self, state: tuple, action: Action) -> float:
        return self.q_values[(state, action)]

    def compute_value(
        self,
        state: tuple,
    ) -> float:

        position = state[0]

        legal_actions = self.get_legal_actions(position)

        if not legal_actions:
            return 0.0

        values = [self.get_Q_value(state, action) for action in legal_actions]

        return max(values)

    def get_legal_actions(
        self,
        position: tuple[int, int],
    ) -> list[Action]:

        legal_actions = []

        for action in Action:
            row_change, column_change = action.value

            next_position = (
                position[0] + row_change,
                position[1] + column_change,
            )

            if self.enviorment.maze.is_valid_move(next_position):
                legal_actions.append(action)

        return legal_actions

    def get_action(
        self,
        state: tuple,
    ) -> Action | None:

        position = state[0]

        legal_actions = self.get_legal_actions(position)

        if not legal_actions:
            return None

        if random.random() < self.exploration_rate:
            action = random.choice(legal_actions)
            return action

        q_values = {
            action: self.get_Q_value(state, action)
            for action in legal_actions
        }

        best_value = max(q_values.values())

        best_actions = [
            action
            for action in legal_actions
            if q_values[action] == best_value
        ]

        action = random.choice(best_actions)

        return action

    def update(
        self, state: tuple, action: Action, next_state: tuple, reward: float, done: bool
    ):
        current_q = self.get_Q_value(state, action)

        if done:
            future_value = 0.0
        else:
            future_value = self.compute_value(next_state)

        target = reward + self.discount_factor * future_value

        difference = target - current_q

        self.q_values[(state, action)] = current_q + self.learning_rate * difference
