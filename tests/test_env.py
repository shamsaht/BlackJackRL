import pytest
import sys
import os

# Add the root of the project (21) to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from blackjack import CustomBlackjackEnv, is_bust, hand_score, basic_strategy

@pytest.fixture
def env():
    """Fixture to initialize the CustomBlackjackEnv environment."""
    return CustomBlackjackEnv()

def test_environment_initialization(env):
    """Test the initialization of the environment."""
    assert env.deck_count == 6, "Deck count should be 6."
    assert len(env.deck) == 312, "Deck should contain 312 cards (6 decks)."
    assert env.player_hands == [], "Player hands should be initialized as an empty list."
    assert env.current_hand_index == 0, "Current hand index should be initialized to 0."

def test_deck_shuffling_and_drawing(env):
    """Test deck shuffling and card drawing functionality."""
    initial_deck = env.deck.copy()
    env.reset_shoe()
    assert env.deck != initial_deck, "Deck should be shuffled differently after reset."
    drawn_card = env.draw_card()
    assert drawn_card in range(1, 12), "Drawn card should be a valid card value."
    assert len(env.deck) == 311, "Deck should have 311 cards after drawing one."

def test_player_actions(env):
    """Test various player actions: hit, stick, double down, and split."""
    env.reset()
    env.player = [10, 6]  # Player starts with a total of 16
    env.dealer = [10, 7]  # Dealer starts with a total of 17

    # Test hit action
    obs, reward, done, _ = env.step(1)  # Player hits
    assert not done or reward == -1, "Game should not be over after a hit if player hasn't busted."

    # Test stick action
    env.player = [10, 7]  # Player has 17
    obs, reward, done, _ = env.step(0)  # Player sticks
    assert done, "Game should be over after sticking."
    assert reward == 0, "Player should lose with 17 against dealer's 17."

    # Test double down action
    env.reset()
    env.player = [5, 6]  # Player has 11
    obs, reward, done, _ = env.step(2)  # Player doubles down
    assert done, "Game should be over after double down."
    assert reward in [-2, 0, 2], "Reward should reflect double down outcome."

    # Test split action
    env.reset()
    env.player = [8, 8]  # Player has a pair of 8s
    obs, reward, done, _ = env.step(3)  # Player splits
    assert len(env.player_hands) == 2, "Player should have two hands after split."
    assert not done, "Game should continue after a split."

def test_reward_logic(env):
    """Test the reward calculation logic."""
    # Player wins
    env.player = [10, 10]  # 20
    env.dealer = [10, 7]   # 17
    reward = env._calculate_reward()
    assert reward == 1, "Player should win with 20 against dealer's 17."

    # Player loses
    env.player = [10, 6]  # 16
    env.dealer = [10, 7]  # 17
    reward = env._calculate_reward()
    assert reward == -1, "Player should lose with 16 against dealer's 17."

    # Push
    env.player = [10, 7]  # 17
    env.dealer = [10, 7]  # 17
    reward = env._calculate_reward()
    assert reward == 0, "Should be a push with both player and dealer at 17."

    # Player busts
    env.player = [10, 10, 2]  # 22
    env.dealer = [10, 7]      # 17
    reward = env._calculate_reward()
    assert reward == -1, "Player should lose if busted."

    # Dealer busts
    env.player = [10, 7]      # 17
    env.dealer = [10, 10, 2]  # 22
    reward = env._calculate_reward()
    assert reward == 1, "Player should win if dealer busts."

def test_basic_strategy_soft_totals():
    # Soft 17, dealer shows 10
    assert basic_strategy([1, 6], 10) == 1, "Should hit on soft 17 vs dealer 10"
    
    # Soft 18, dealer shows 6
    assert basic_strategy([1, 7], 6) == 2, "Should double down on soft 18 vs dealer 6"

    # Soft 18, dealer shows 8
    assert basic_strategy([1, 7], 8) == 0, "Should stick on soft 18 vs dealer 8"

    # Soft 19, dealer shows any card
    assert basic_strategy([1, 8], 9) == 0, "Should stick on soft 19 vs dealer 9"

def test_full_game():
    env = CustomBlackjackEnv()
    env.reset()
    done = False
    while not done:
        action = basic_strategy(env.player, env.dealer[0])  # Use basic strategy
        obs, reward, done, _ = env.step(action)
    assert reward in [-1, 0, 1], "Reward should be valid at the end of the game."

def test_player_busts_after_hit():
    env = CustomBlackjackEnv()
    env.reset()
    env.player = [10, 10]  # 20
    env.dealer = [10]  # Dealer shows 10
    
    obs, reward, done, _ = env.step(1)  # Player hits
    assert is_bust(env.player), "Player should bust if they exceed 21."
    assert done, "Game should end after player busts."
    assert reward == -1, "Player should lose if they bust."


def test_split_logic_with_multiple_hands():
    env = CustomBlackjackEnv()
    env.player = [8, 8]  # Splittable hand
    env.dealer = [1]
    env.split_hand()
    assert len(env.player_hands) == 2, "Player should have two hands after splitting."
    print(env.player)
    obs, reward, done, _ = env.step(1)  # Hit on first hand
    print(env.player)
    assert len(env.player) > 2, "Player should have more than two cards after a hit."

def test_performance():
    env = CustomBlackjackEnv()
    rounds = 10000
    wins, losses, pushes = 0, 0, 0
    for _ in range(rounds):
        env.reset()
        done = False
        while not done:
            action = basic_strategy(env.player, env.dealer[0])
            obs, reward, done, _ = env.step(action)
        if reward == 1:
            wins += 1
        elif reward == -1:
            losses += 1
        else:
            pushes += 1
    assert wins + losses + pushes == rounds, "All rounds should result in a valid outcome."

import matplotlib.pyplot as plt

def test_reward_distribution():
    env = CustomBlackjackEnv()
    rewards = []
    for _ in range(1000):
        env.reset()
        done = False
        while not done:
            action = basic_strategy(env.player, env.dealer[0])
            obs, reward, done, _ = env.step(action)
        rewards.append(reward)
    plt.hist(rewards, bins=10, edgecolor='k')
    plt.title("Reward Distribution")
    plt.xlabel("Reward")
    plt.ylabel("Frequency")
    plt.show()

def test_invalid_action_after_session_done():
    env = CustomBlackjackEnv()
    env.reset()
    env.player = [10, 7]  # Player total = 17
    env.dealer = [10]  # Dealer total = 10
    obs, reward, done, _ = env.step(0)  # Stick
    assert done, "Session should be marked as done after the player sticks."

    # Attempt to double down after the session is done
    obs, reward, done, info = env.step(2)
    assert done, "Session should remain marked as done."
    assert reward == 0, "No reward should be applied for actions after session ends."
