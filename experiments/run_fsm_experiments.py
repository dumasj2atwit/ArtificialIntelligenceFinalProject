import csv
import time
from pathlib import Path

from agents.fsm_agent import FSMAgent, FSMState
from environment.environment import MazeEnvironment


MAX_STEPS = 5000

MAZE_DIRECTORY = Path("mazes/experiments")
DIFFICULTIES = ["easy", "medium", "hard"]


def run_fsm_trial(
    difficulty: str,
    maze_file: str,
    trial: int,
) -> dict:
    env = MazeEnvironment(maze_file)
    agent = FSMAgent(env)

    agent.reset()

    success = False

    start_time = time.perf_counter()

    for _ in range(MAX_STEPS):
        if env.robot.reached_goal():
            success = True
            agent.state = FSMState.FINISHED
            break

        action = agent.choose_action()

        if action is None:
            break

        _, _, done = env.step(action)

        if done:
            success = True
            agent.state = FSMState.FINISHED
            break

    end_time = time.perf_counter()

    completion_time = end_time - start_time

    return {
        "solver": "FSM+A*",
        "difficulty": difficulty,
        "maze": maze_file,
        "trial": trial,
        "success": success,
        "steps": env.robot.steps,
        "visited_cells": len(agent.visited),
        "discovered_cells": len(env.discovered),
        "dead_ends": agent.dead_ends,
        "backtrack_steps": agent.backtrack_steps,
        "completion_time_seconds": completion_time,
    }


def main() -> None:
    results = []


    for difficulty in DIFFICULTIES:
        maze_files = sorted(
            MAZE_DIRECTORY.glob(f"{difficulty}_*.txt")
        )

        for trial, maze_path in enumerate(maze_files, start=1):
            result = run_fsm_trial(
                difficulty,
                str(maze_path),
                trial,
            )

            results.append(result)

            print(
                f"{difficulty.upper()} "
                f"Trial {trial}: "
                f"Success={result['success']} "
                f"Steps={result['steps']} "
                f"Time={result['completion_time_seconds']:.6f}s"
            )


    output_path = Path("results/fsm_results.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "solver",
        "difficulty",
        "maze",
        "trial",
        "success",
        "steps",
        "visited_cells",
        "discovered_cells",
        "dead_ends",
        "backtrack_steps",
        "completion_time_seconds",
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