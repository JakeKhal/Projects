import random

# Create a deck of cards
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

deck = []
for suit in suits:
    for rank in ranks:
        deck.append(rank)

# Function to calculate the total value of a hand
def calculate_hand_value(hand):
    value = 0
    num_aces = 0

    for card in hand:
        rank = card[:-1]

        if rank.isdigit():
            value += int(rank)
        elif rank == 'A':
            value += 11
            num_aces += 1
        else:
            value += 10

    while value > 21 and num_aces > 0:
        value -= 10
        num_aces -= 1

    return value

# Function to deal a card
def deal_card():
    card = random.choice(deck)
    deck.remove(card)
    return card

# Game setup
player_hand = [deal_card(), deal_card()]
dealer_hand = [deal_card()]

# Game loop
while True:
    # Display player's hand and value
    print("Player's Hand:", player_hand, "Value:", calculate_hand_value(player_hand))

    # Display dealer's hand
    print("Dealer's Hand:", [dealer_hand[0], '???'])

    # Check if player or dealer has blackjack
    if calculate_hand_value(player_hand) == 21 and calculate_hand_value(dealer_hand) == 21:
        print("Push! Both player and dealer have blackjack.")
        break
    elif calculate_hand_value(player_hand) == 21:
        print("Player wins with blackjack!")
        break
    elif calculate_hand_value(dealer_hand) == 21:
        print("Dealer wins with blackjack!")
        break

    # Ask the player to hit or stand
    action = input("Do you want to (h)it or (s)tand? ")

    # Player hits
    if action.lower() == 'h':
        player_hand.append(deal_card())

        # Check if player busts
        if calculate_hand_value(player_hand) > 21:
            print("Player busts! Dealer wins.")
            break

    # Player stands
    elif action.lower() == 's':
        # Dealer's turn
        while calculate_hand_value(dealer_hand) < 17:
            dealer_hand.append(deal_card())

        # Display dealer's hand and value
        print("Dealer's Hand:", dealer_hand, "Value:", calculate_hand_value(dealer_hand))

        # Check if dealer busts
        if calculate_hand_value(dealer_hand) > 21:
            print("Dealer busts! Player wins.")
        elif calculate_hand_value(player_hand) > calculate_hand_value(dealer_hand):
            print("Player wins!")
        elif calculate_hand_value(player_hand) < calculate_hand_value(dealer_hand):
            print("Dealer wins.")
        else:
            print("Push! It's a tie.")

        break

    # Invalid input
    else:
        print("Invalid input. Please try again.")
