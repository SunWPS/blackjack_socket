import random


deck = {"A": 4, "2": 4, "3": 4, "4": 4, "5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 4, "J": 4, "Q": 4, "K": 4}
card_score = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10,
              "K": 10}


def re_deck():
    for k, v in deck.items():
        deck[k] = 4


def pick_card():
    # empty deck
    if sum(deck.values()) == 0:
        return 0

    card = random.choice(list(deck.keys()))
    while deck[card] <= 0:
        card = random.choice(list(deck.keys()))

    deck[card] -= 1
    return card


def calculate_score(cards):
    score = sum([card_score[card] for card in cards])

    # a a q
    if "A" in cards:
        if score > 21:
            score -= 10
    return score


def result(user_card, host_card):
    user_score = calculate_score(user_card)
    host_score = calculate_score(host_card)

    if user_score == host_score:
        return "Draw"
    elif user_score > 21:
        return "You Lose"
    elif host_score > 21:
        return "You Win"
    elif user_score > host_score and user_score <= 21:
        return "You Win"
    elif user_score < host_score and host_score <= 21:
        return "You Lose"
   
    
def check_busted(score):
    if score > 21:
        return True
    return False


def check_host(host_card):
    return False if calculate_score(host_card) >= 17 else True


def check_blackjack(picked_card):
    blackjack = False
    if "A" in picked_card:
        for card in picked_card:
            if card in ['J', 'Q', 'K', 'A']:
                blackjack = True
            else:
                blackjack = False
                break
    return blackjack

def open_card(user_card, host_card):
    return "Your final hand is :" + str(user_card) + ", and score is: " + str(calculate_score(user_card)) + \
    "\nHost's hand is : " + str(host_card) + ", and score is: " + str(calculate_score(host_card))
