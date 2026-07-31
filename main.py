import time

from agents.fsm_agent import FSMAgent, FSMState
from environment.environment import MazeEnvironment


def main() -> None:
    env = MazeEnvironment("mazes/easy.txt")
    agent = FSMAgent(env)

    agent.reset()

    max_steps = 500

    for _ in range(max_steps):
        print("\n" * 2)
        print(f"Current State: {agent.state.name}")
        print(f"Current Position: {env.robot.position}")
        env.render()

        if env.robot.reached_goal():
            agent.state = FSMState.FINISHED

            print("\n===== FSM RESULTS =====")
            print("Goal Reached: Yes")
            print(f"Steps Taken: {env.robot.steps}")
            print(f"Visited Cells: {len(agent.visited)}")
            print(f"Dead Ends: {agent.dead_ends}")
            print(f"Backtrack Steps: {agent.backtrack_steps}")
            break

        action = agent.choose_action()

        if action is None:
            print("\nThe FSM could not find the goal.")
            break

        _, _, done = env.step(action)

        time.sleep(0.15)

        if done:
            print("\n" * 2)
            print(f"Current State: {agent.state.name}")
            print(f"Current Position: {env.robot.position}")
            env.render()

            print("\n===== FSM RESULTS =====")
            print("Goal Reached: Yes")
            print(f"Steps Taken: {env.robot.steps}")
            print(f"Visited Cells: {len(agent.visited)}")
            print(f"Dead Ends: {agent.dead_ends}")
            print(f"Backtrack Steps: {agent.backtrack_steps}")
            break
    else:
        print("\nMaximum step count reached.")


if __name__ == "__main__":
    main()