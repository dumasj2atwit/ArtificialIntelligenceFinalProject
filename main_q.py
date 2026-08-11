import time

from agents.q_learning_agent import QLearningAgent
from environment.environment import MazeEnvironment
from training.train_q_learning import train_q_learning


def run_learned_agent(
    agent: QLearningAgent,
    environment: MazeEnvironment,
    # renderer: PyGameRenderer,
):
    agent.enviorment = environment
    environment.reset()

    state = agent.get_state()

    print("Start position:", environment.robot.position)
    print("Legal actions:", agent.get_legal_actions(environment.robot.position))

    total_reward = 0
    steps = 0
    done = False

    # No exploration after training.
    agent.exploration_rate = 0

    while not done and steps < 500:

        # if not renderer.process_events():
        #     return

        # renderer.render(environment.robot)

        action = agent.get_action(
            state,
        )

        print(
            f"Step {steps}: "
            f"position={environment.robot.position}, "
            f"action={action}"
        )

        if action is None:
            break

        _, reward, done = environment.step(action)

        next_state = agent.get_state()
        print("Start position:", environment.robot.position)
        print("Legal actions:", agent.get_legal_actions(environment.robot.position))

        state = next_state

        total_reward += reward
        steps += 1

        time.sleep(0.15)

    # renderer.render(environment.robot)

    print("\n===== Q-LEARNING RESULTS =====")
    print(f"Goal Reached: {done}")
    print(f"Steps Taken: {steps}")
    print(f"Total Reward: {total_reward}")
    print(f"Visited Cells: " f"{len(environment.robot.visited_positions)}")

    time.sleep(2)


def main():

    maze_file = "mazes/easy.txt"

    print("Training Q-learning agent...")

    (
        agent,
        rewards,
        steps,
        successes,
    ) = train_q_learning(
        maze_file,
        episodes=1000,
    )

    print("\nTraining complete.")

    environment = MazeEnvironment(maze_file)
    # renderer = PyGameRenderer(environment.maze)

    run_learned_agent(
        agent,
        environment,
        # renderer,
    )


if __name__ == "__main__":
    main()
