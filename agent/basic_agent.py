class BasicStrategyAgent:
    def choose_action(self, state):
        """
        Determine the action based on the basic strategy.
        Args:
            state: Tuple (player_total, dealer_card, usable_ace, player_cards).
        Returns:
            int: Action (0 = Stick, 1 = Hit, 2 = Double Down, 3 = Split).
        """
        player_total, dealer_card, usable_ace, player_cards = state

        # Splitting logic
        if len(player_cards) == 2 and player_cards[0] == player_cards[1]:
            if player_cards[0] in [8, 1]:  # Always split Aces and 8s
                return 3
            elif player_cards[0] == 10 or player_cards[0] == 5:  # Never split 10s or 5s
                return 0
            elif player_cards[0] == 9 and dealer_card not in [7, 10, 1]:  # Split 9s unless dealer shows 7, 10, or Ace
                return 3
            elif player_cards[0] == 6 and dealer_card in [2, 3, 4, 5, 6]:  # Split 6s if dealer shows 2-6
                return 3

        # Soft totals (usable Ace)
        if usable_ace:
            if player_total <= 17:
                return 1  # Hit
            elif player_total == 18:
                if dealer_card in [3, 4, 5, 6]:
                    return 2  # Double down
                elif dealer_card in [2, 7, 8]:
                    return 0  # Stick
                else:
                    return 1  # Hit
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
            return 2 if len(player_cards) == 2 else 1  # Double down only on first two cards
        elif player_total == 9 and dealer_card in [3, 4, 5, 6]:
            return 2 if len(player_cards) == 2 else 1  # Double down only on first two cards
        else:
            return 1  # Hit
