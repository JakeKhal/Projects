import random

ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['♠', '♥', '♦', '♣']
deck = []

for suit in suits:
    for rank in ranks:
        card = rank + suit
        deck.append(card)

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

def deal_card():
    card = random.choice(deck)
    deck.remove(card)
    return card

player_hand = [deal_card(), deal_card()]
dealer_hand = [deal_card()]

while True:
    print("Player:", player_hand, "Value:", calculate_hand_value(player_hand))
    print("Dealer:", [dealer_hand[0], '???'])

    if calculate_hand_value(player_hand) == 21 and calculate_hand_value(dealer_hand) == 21:
        print("Push!")
        break
    elif calculate_hand_value(player_hand) == 21:
        print("Player wins with blackjack!")
        break
    elif calculate_hand_value(dealer_hand) == 21:
        print("Dealer wins with blackjack!")
        break

    action = input("hit or stand? (h/s) ")

    if action.lower() == 'h':
        player_hand.append(deal_card())

        if calculate_hand_value(player_hand) > 21:
            print("Player busts! Dealer wins.")
            break

    elif action.lower() == 's':
        while calculate_hand_value(dealer_hand) < 17:
            dealer_hand.append(deal_card())
            print("Dealer's Hand:", dealer_hand)

        print("Dealer's Hand:", dealer_hand)

        if calculate_hand_value(dealer_hand) > 21:
            print("Dealer busts! Player wins.")
        elif calculate_hand_value(player_hand) > calculate_hand_value(dealer_hand):
            print("Player wins!")
        elif calculate_hand_value(player_hand) < calculate_hand_value(dealer_hand):
            print("Dealer wins.")
        else:
            print("Push! It's a tie.")

        break

    else:
        print("Invalid input. Please try again.")
