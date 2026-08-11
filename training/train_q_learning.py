from agents.q_learning_agent import QLearningAgent
from environment.environment import MazeEnvironment


def train_q_learning(
    maze_file: str,
    episodes: int = 1000,
):

    environment = MazeEnvironment(maze_file)

    agent = QLearningAgent(
        enviorment=environment,
        learning_rate=0.2,
        discount_factor=0.9,
        exploration_rate=1.0,
    )

    rewards = []
    steps = []
    successes = []

    for episode in range(episodes):

        environment.reset()

        state = agent.get_state()

        total_reward = 0
        episode_steps = 0
        done = False
        #and episode_steps < 1000
        while not done:

            action = agent.get_action(state)

            if action is None:
                break

            _, reward, done = environment.step(action)

            next_state = agent.get_state()

            agent.update(
                state,
                action,
                next_state,
                reward,
                done,
            )

            state = next_state

            total_reward += reward
            episode_steps += 1

        rewards.append(total_reward)
        steps.append(episode_steps)
        successes.append(done)

        if (episode + 1) % 50 == 0:
            print(
            f"Episode {episode + 1}: "
            f"Steps={episode_steps}, "
            f"Reward={total_reward}, "
            f"Success={done}"
        )

        # Decay exploration
        agent.exploration_rate = max(
            0.05,
            agent.exploration_rate * 0.995,
        )

    return agent, rewards, steps, successes