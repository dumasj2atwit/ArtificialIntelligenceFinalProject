import time

from agents.fsm_agent import FSMAgent, FSMState
from environment.environment import MazeEnvironment
from visualization.render import PyGameRenderer


def main() -> None:
    env = MazeEnvironment("mazes/hard.txt")
    agent = FSMAgent(env)
    renderer = PyGameRenderer(env.maze, env.robot)

    agent.reset()

    # renderer = PyGameRenderer(env.maze)

    max_steps = 500

    try:
        for _ in range(max_steps):

            # Allow the Pygame window to close normally.
            if not renderer.process_events():
                return

            # Draw current robot position.
            renderer.render(env.robot)

            print("\n" * 2)
            print(f"Cells Discovered: {len(env.discovered)}")
            print(f"Current State: {agent.state.name}")
            print(f"Current Position: {env.robot.position}")
            print(f"Goal discovered: {env.goal_discovered()}")

            if env.robot.reached_goal():
                agent.state = FSMState.FINISHED

                print("\n===== FSM RESULTS =====")
                print("Goal Reached: Yes")
                print(f"Steps Taken: {env.robot.steps}")
                print(f"Visited Cells: {len(agent.visited)}")
                print(f"Dead Ends: {agent.dead_ends}")
                print(f"Backtrack Steps: {agent.backtrack_steps}")

                # renderer.render(env.robot)
                break

            action = agent.choose_action()

            if action is None:
                print("\nThe FSM could not find the goal.")
                break

            _, _, done = env.step(action)

            time.sleep(0.15)

            if done:
                agent.state = FSMState.FINISHED

                renderer.render(env.robot)

                print("\n===== FSM RESULTS =====")
                print("Goal Reached: Yes")
                print(f"Steps Taken: {env.robot.steps}")
                print(f"Visited Cells: {len(agent.visited)}")
                print(f"Dead Ends: {agent.dead_ends}")
                print(f"Backtrack Steps: {agent.backtrack_steps}")
                break

        else:
            print("\nMaximum step count reached.")
        # Leave the finished maze visible briefly.
        renderer.render(env.robot)
        time.sleep(2)
    finally:
        # renderer.close()
        pass


if __name__ == "__main__":
    main()