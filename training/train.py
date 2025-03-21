#!/usr/bin/env python3
def train_agent(env, agent, episodes=50000):
    rewards = []
    for episode in range(episodes):
        obs = env.reset()
        player_total, dealer_card, usable_ace = obs
        player_cards = env.player
        state = agent.state_representation(player_total, dealer_card, usable_ace, player_cards)
        done = False
        total_reward = 0
        
        while not done:
            action = agent.choose_action(state)
            next_obs, reward, done, _ = env.step(action)
            next_player_total, next_dealer_card, next_usable_ace = next_obs
            next_player_cards = env.player
            next_state = agent.state_representation(next_player_total, next_dealer_card, next_usable_ace, next_player_cards)

            agent.update(state, action, reward, next_state, done)

            state = next_state
            total_reward += reward

        rewards.append(total_reward)

        if episode % 1000 == 0:
            print(f"Episode {episode}/{episodes} - Total Reward: {total_reward}")

    return rewards
