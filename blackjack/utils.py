#!/usr/bin/env python3
def is_bust(hand):
    """Determine if a hand is bust."""
    score, _ = hand_score(hand)
    return score > 21


def hand_score(hand):
    """
    Calculate the total score of a blackjack hand and determine if it contains a usable ace.
    
    Args:
        hand (list): List of integers representing the cards in hand.
        
    Returns:
        tuple: (score, usable_ace)
            - score (int): Total value of the hand.
            - usable_ace (bool): True if the hand contains an ace counted as 11 without busting.
    """
    total = sum(hand)
    usable_ace = 1 in hand and total + 10 <= 21
    if usable_ace:
        total += 10
    return total, usable_ace

def basic_strategy(player_hand, dealer_card):
    """
    Determine the optimal action based on the basic strategy.
    Args:
        player_hand (list): The player's hand (list of card values).
        dealer_card (int): The value of the dealer's visible card.
    Returns:
        int: Action to take (0 = Stick, 1 = Hit, 2 = Double Down, 3 = Split).
    """
    player_total, usable_ace = hand_score(player_hand)
    
    # Splitting logic
    if len(player_hand) == 2 and player_hand[0] == player_hand[1]:
        if player_hand[0] == 8 or player_hand[0] == 1:  # Always split Aces and 8s
            return 3
        elif player_hand[0] == 10 or player_hand[0] == 5:  # Never split 10s or 5s
            return 0
        elif player_hand[0] == 9 and dealer_card not in [7, 10, 1]:  # Split 9s unless dealer shows 7, 10, or Ace
            return 3
        elif player_hand[0] == 6 and dealer_card in [2, 3, 4, 5, 6]:  # Split 6s if dealer shows 2-6
            return 3

    # Soft totals (usable Ace)
    if usable_ace:
        if player_total <= 17:
            return 1  # Hit
        elif player_total == 18:
            return 0 if dealer_card in [2, 7, 8] else 2 if dealer_card <= 6 else 1  # Stick on 2, 7, 8; Hit otherwise
        else:
            return 0  # Stick on soft 19+

    # Hard totals
    if player_total >= 17:
        return 0  # Stick
    elif 13 <= player_total <= 16 and dealer_card in [2, 3, 4, 5, 6]:
        return 0  # Stick if dealer has 2-6
    elif player_total == 12 and dealer_card in [4, 5, 6]:
        return 0  # Stick if dealer has 4-6
    elif player_total == 11 or (player_total == 10 and dealer_card < 10):  # Double Down
        return 2 if len(player_hand) == 2 else 1  # Double down only on first two cards
    elif player_total == 9 and dealer_card in [3, 4, 5, 6]:
        return 2 if len(player_hand) == 2 else 1  # Double down only on first two cards
    else:
        return 1  # Hit

