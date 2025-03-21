#!/usr/bin/env python3
from blackjack.custom_env import CustomBlackjackEnv
from training import train_agent, evaluate_agents, evaluate_and_compare_agents
from agent import BasicStrategyAgent, QLearningAgent

def main():
    

    actions = [0, 1, 2, 3]  # Stick, Hit, Double Down, Split

    env = CustomBlackjackEnv()
    q_agent = QLearningAgent(actions=actions, alpha=0.7, gamma=1.0, epsilon=1.0)
    basic_agent = BasicStrategyAgent()

    # Train Q-Learning Agent
    print("Training the Q-Learning Agent...")
    episodes = 50000000
    train_agent(env, q_agent, episodes=episodes)

    # Evaluate Agents
    print("Evaluating Agents...")
    #q_avg_reward, basic_avg_reward =
    q_agent.epsilon = 0
    evaluate_and_compare_agents(env, q_agent, basic_agent, 1000)

    #print("\nComparison:")
    #print(f"Q-Learning Agent Average Reward: {q_avg_reward}")
    #print(f"Basic Strategy Agent Average Reward: {basic_avg_reward}")


if __name__ == "__main__":
    main()
