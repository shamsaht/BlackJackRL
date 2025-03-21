import numpy as np
import random
from collections import defaultdict

class QLearningAgent:
    def __init__(self, actions, alpha=0.05, gamma=0.99, epsilon=1.0, epsilon_decay=0.9995, epsilon_min=0.1):
        """
        Q-Learning Agent
        Args:
            actions: List of possible actions.
            alpha: Learning rate.
            gamma: Discount factor.
            epsilon: Exploration rate.
        """
        self.q_table = defaultdict(lambda: np.zeros(len(actions)))
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

    def state_representation(self, player_total, dealer_card, usable_ace, player_cards):
        """Convert the game state into a unique representation."""
        return (player_total, dealer_card, usable_ace, tuple(sorted(player_cards)))

    def choose_action(self, state):
        """Choose action based on epsilon-greedy policy."""
        if random.random() < self.epsilon:
            return random.choice(self.actions)  # Explore
        else:
            return np.argmax(self.q_table[state])  # Exploit

    def update(self, state, action, reward, next_state, done):
        """Update Q-value using the Q-Learning update rule."""
        q_predict = self.q_table[state][action]
        if done:
            q_target = reward  # No next state if terminal
        else:
            q_target = reward + self.gamma * np.max(self.q_table[next_state])
        self.q_table[state][action] += self.alpha * (q_target - q_predict)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        self.alpha = max(0.001, self.alpha * 0.99)
