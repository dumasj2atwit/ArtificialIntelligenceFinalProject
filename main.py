from environment.maze import Maze
from environment.robot import Action, Robot


KEYBOARD_ACTIONS = {
    "w": Action.UP,
    "d": Action.RIGHT,
    "s": Action.DOWN,
    "a": Action.LEFT,
}


def main() -> None:
    maze = Maze("mazes/easy.txt")
    robot = Robot(maze)

    print("Move with W, A, S, and D.")
    print("Enter Q to quit.")

    while True:
        print()
        maze.display(robot.position)

        if robot.reached_goal():
            print(f"\nGoal reached in {robot.steps} steps!")
            break

        command = input("\nMove: ").strip().lower()

        if command == "q":
            print("Simulation ended.")
            break

        action = KEYBOARD_ACTIONS.get(command)

        if action is None:
            print("Invalid command. Use W, A, S, D, or Q.")
            continue

        moved = robot.move(action)

        if not moved:
            print("The robot cannot move through a wall.")


if __name__ == "__main__":
    main()