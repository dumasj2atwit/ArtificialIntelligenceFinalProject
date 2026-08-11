import csv
import time
from pathlib import Path

from environment.environment import MazeEnvironment
from training.train_q_learning import train_q_learning


MAZE_DIRECTORY = Path("mazes/experiments")
DIFFICULTIES = ["easy", "medium", "hard"]

TRAINING_EPISODES = 1000
MAX_EVALUATION_STEPS = 5000


def evaluate_agent(
    maze_file: str,
    difficulty: str,
    trial: int,
) -> dict:
    # Train a fresh agent on this maze
    agent, rewards, training_steps, successes = train_q_learning(
        maze_file,
        episodes=TRAINING_EPISODES,
    )

    environment = MazeEnvironment(maze_file)
    environment.reset()

    # Disable exploration for final evaluation.
    agent.enviorment = environment
    agent.exploration_rate = 0.0

    state = agent.get_state()

    success = False
    total_reward = 0
    evaluation_steps = 0

    start_time = time.perf_counter()

    while evaluation_steps < MAX_EVALUATION_STEPS:
        if environment.robot.reached_goal():
            success = True
            break

        action = agent.get_action(state)

        if action is None:
            break

        _, reward, done = environment.step(action)

        next_state = agent.get_state()

        state = next_state
        total_reward += reward
        evaluation_steps += 1

        if done:
            success = True
            break

    end_time = time.perf_counter()

    return {
        "solver": "Q-Learning",
        "difficulty": difficulty,
        "maze": maze_file,
        "trial": trial,
        "success": success,
        "steps": evaluation_steps,
        "visited_cells": len(environment.robot.visited_positions),
        "discovered_cells": len(environment.discovered),
        "total_reward": total_reward,
        "completion_time_seconds": end_time - start_time,
        "training_episodes": TRAINING_EPISODES,
        "training_success_rate": (
            sum(successes) / len(successes)
            if successes
            else 0.0
        ),
        "final_training_reward": rewards[-1] if rewards else 0,
    }


def main() -> None:
    results = []

    for difficulty in DIFFICULTIES:
        maze_files = sorted(
            MAZE_DIRECTORY.glob(f"{difficulty}_*.txt")
        )

        for trial, maze_path in enumerate(maze_files, start=1):
            print(
                f"Training Q-learning on "
                f"{maze_path.name}..."
            )

            result = evaluate_agent(
                str(maze_path),
                difficulty,
                trial,
            )

            results.append(result)

            print(
                f"{difficulty.upper()} "
                f"Trial {trial}: "
                f"Success={result['success']} "
                f"Steps={result['steps']} "
                f"Reward={result['total_reward']} "
                f"Time={result['completion_time_seconds']:.6f}s"
            )

    output_path = Path("results/rl_results.csv")
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "solver",
        "difficulty",
        "maze",
        "trial",
        "success",
        "steps",
        "visited_cells",
        "discovered_cells",
        "total_reward",
        "completion_time_seconds",
        "training_episodes",
        "training_success_rate",
        "final_training_reward",
    ]

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(results)

    print()
    print(f"Results saved to {output_path}")


if __name__ == "__main__":
    main()