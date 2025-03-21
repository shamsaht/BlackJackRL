#!/usr/bin/env python3
import numpy as np
def evaluate_agents(env, q_agent, basic_agent, episodes=1000):
    q_agent_rewards = []
    basic_agent_rewards = []

    for _ in range(episodes):
        # Evaluate Q-Learning Agent
        env.reset()
        obs = env._get_obs()
        player_total, dealer_card, usable_ace = obs
        player_cards = env.player
        q_state = q_agent.state_representation(player_total, dealer_card, usable_ace, player_cards)
        done = False
        q_total_reward = 0

        while not done:
            action = np.argmax(q_agent.q_table[q_state])  # Q-Agent's action
            obs, reward, done, _ = env.step(action)
            player_total, dealer_card, usable_ace = obs
            player_cards = env.player
            q_state = q_agent.state_representation(player_total, dealer_card, usable_ace, player_cards)
            q_total_reward += reward

        q_agent_rewards.append(q_total_reward)

        # Evaluate Basic Strategy Agent
        env.reset()
        obs = env._get_obs()
        player_total, dealer_card, usable_ace = obs
        player_cards = env.player
        b_state = (player_total, dealer_card, usable_ace, tuple(sorted(player_cards)))
        done = False
        b_total_reward = 0

        while not done:
            action = basic_agent.choose_action(b_state)  # Basic strategy action
            obs, reward, done, _ = env.step(action)
            player_total, dealer_card, usable_ace = obs
            player_cards = env.player
            b_state = (player_total, dealer_card, usable_ace, tuple(sorted(player_cards)))
            b_total_reward += reward

        basic_agent_rewards.append(b_total_reward)

    # Calculate and compare average rewards
    q_avg_reward = np.mean(q_agent_rewards)
    basic_avg_reward = np.mean(basic_agent_rewards)

    print(f"Q-Learning Agent Average Reward: {q_avg_reward}")
    print(f"Basic Strategy Agent Average Reward: {basic_avg_reward}")
    return q_avg_reward, basic_avg_reward

import random

def evaluate_and_compare_agents(env, q_agent, basic_agent, num_tests=1000):
    """
    Compare the actions of the Q-Learning agent and the Basic Strategy agent.
    Args:
        env: The environment.
        q_agent: The trained Q-Learning agent.
        basic_agent: The rule-based Basic Strategy agent.
        num_tests: Number of random states to evaluate.

    Returns:
        None
    """
    mismatches = 0  # Count of mismatches
    total_tests = 0

    print("\nEvaluation Results:")

    for _ in range(num_tests):
        # Generate a random test state
        env.reset()
        player_total, dealer_card, usable_ace = env._get_obs()
        player_cards = env.player
        state = (player_total, dealer_card, usable_ace, tuple(sorted(player_cards)))

        # Get actions from both agents
        q_action = np.argmax(q_agent.q_table[q_agent.state_representation(*state)])
        basic_action = basic_agent.choose_action(state)

        # Compare actions
        if q_action != basic_action:
            mismatches += 1
            print(q_agent.q_table[q_agent.state_representation(*state)])
            print(f"\033[91mMismatch: State: {state}, Q-Agent: {q_action}, Basic-Agent: {basic_action}\033[0m")  # Red output
        else:
            print(f"Match: State: {state}, Q-Agent: {q_action}, Basic-Agent: {basic_action}")

        total_tests += 1

    # Summary
    print("\nSummary:")
    print(f"Total Tests: {total_tests}")
    print(f"Total Mismatches: {mismatches}")
    print(f"Accuracy: {(1 - mismatches / total_tests) * 100:.2f}%")
