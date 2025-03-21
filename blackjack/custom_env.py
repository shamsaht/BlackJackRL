from blackjack.utils import is_bust, hand_score, basic_strategy
import gym
from gym.envs.toy_text.blackjack import BlackjackEnv  # Import the base BlackjackEnv
# from blackjack.utils import is_bust, score_hand  # Import utility functions
import numpy as np

class CustomBlackjackEnv(BlackjackEnv):
    def __init__(self):
        super().__init__(natural=True)
        self.deck_count = 6
        self.deck = []  # Initialize the deck attribute
        self.reset_shoe() 
        self.dealer = []
        self.done = False
        # self.reset() # Reset the shoe when the environment is created

    def reset(self):
        """Reset the environment, shuffle the shoe if needed, and deal cards in the correct order."""
        # Reset the player and dealer hands
        self.player = [self.draw_card()]  # Player gets the first card
        self.dealer = [self.draw_card()]  # Dealer gets their first card
        self.player.append(self.draw_card())  # Player gets their second card
        self.done = False
        return self._get_obs()

    def reset_shoe(self):
        """Reset the shoe with a shuffled 6-deck set."""
        self.deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4 * self.deck_count
        np.random.shuffle(self.deck)
        self.player_hands = []
        self.current_hand_index = 0

    def draw_card(self):
        """Draw a card from the shoe."""
        if len(self.deck) < 40 : 
            self.reset_shoe()
        return self.deck.pop()

    def step(self, action):
        """
        Perform the selected action.
        Actions:
        0 - Stick (Hold)
        1 - Hit
        2 - Double Down
        3 - Split
        """
        if hasattr(self, 'done') and self.done:
            return self._get_obs(), 0, True, {}
        if action == 2:  # Double Down
            self.player.append(self.draw_card())
            done = True
            self.play_dealer_hand()
            reward = self._calculate_reward() * 2
            return self._get_obs(), reward, done, {}
        elif action == 3:  # Split
            if len(self.player) == 2 and self.player[0] == self.player[1]:
                self.split_hand()
            else:
                reward = -50  # Arbitrary penalty
                done = True
                return self._get_obs(), reward, done, {}
            # Return the observation for the first split hand
            return self._get_obs(), 0, False, {}
        
        # elif action == 1:  # Hit
        #     self.player.append(self.draw_card())
        #     if is_bust(self.player):  # Player busts
        #         reward = self._calculate_reward()
        #         done = True
        #         return self._get_obs(), reward, done, {}
        #     else:  # Player can continue
        #         return self._get_obs(), 0, False, {}
        # For Hit (1) and Stick (0), continue standard gameplay
        obs, reward, done, info = super().step(action)
        reward *= 10
        if done and action != 1:  # Current hand is finished
            if self.current_hand_index < len(self.player_hands) - 1:
                self._advance_to_next_hand()
                done = False  # Continue the game with the next hand
                
                # Game continues with the next round
        if done :
            if len(self.deck) < 15 : 
                    self.reset_shoe()
        self.done = done
        return obs, reward, done, info

    def play_dealer_hand(self):
        """Play the dealer's hand according to blackjack rules."""
        while True:
            dealer_score, _ = hand_score(self.dealer)  # Calculate dealer's score
            if dealer_score >= 17:  # Dealer stands on 17 or higher
                break
            self.dealer.append(self.draw_card())  # Dealer hits

    def split_hand(self):
        """Split the player's current hand into two."""
        card = self.player.pop()
        self.player_hands.append([card, self.draw_card()])  # Add new hand
        self.player.append(self.draw_card())  # Replace card in the original hand
        self.player_hands.append(self.player)
        self.player = self.player_hands[self.current_hand_index] # Update the current hand

    def _advance_to_next_hand(self):
        """Move to the next hand in the player's split hands."""
        self.current_hand_index += 1
        if self.current_hand_index < len(self.player_hands):
            self.player = self.player_hands[self.current_hand_index]

    def calculate_cumulative_reward(self):
        """Calculate the cumulative reward for all hands."""
        total_reward = 0
        for hand in self.player_hands:
            self.player = hand
            total_reward += self._calculate_reward()
        return total_reward

    def _calculate_reward(self):
        """Calculate the reward based on the current game state."""
        if is_bust(self.player):
            return -10  # Double down penalty if bust

        if is_bust(self.dealer):
            return 10  # Double down reward if dealer busts

        player_total,_ = hand_score(self.player)
        dealer_total,_ = hand_score(self.dealer)

        if player_total > dealer_total:
            return  10  # Player wins
        elif player_total < dealer_total:
            return -10  # Dealer wins
        else:
            return 0  # Push
        
    def _start_next_round(self):
        """Prepare for the next round by dealing new cards."""
        self.player = [self.draw_card(), self.draw_card()]  # New cards for the player
        self.dealer = [self.draw_card()]  # New card for the dealer
        self.current_hand_index = 0
        self.player_hands = []
