# Wongsakorn Pinvasee 6210400175
# Tananat Kometjamikorn 6210406581

import random


CARD_SCORE = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10,
              "K": 10}


def re_deck(deck):
    for k, v in deck.items():
        deck[k] = 4
    return deck


def pick_card(deck):

    if sum(deck.values()) == 0:
        return 0

    card = random.choice(list(deck.keys()))
    while deck[card] <= 0:
        card = random.choice(list(deck.keys()))

    deck[card] -= 1
    return card


def calculate_score(cards):
    score = sum([CARD_SCORE[card] for card in cards])
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
    elif host_score < user_score <= 21:
        return "You Win"
    elif user_score < host_score <= 21:
        return "You Lose"


def check_busted(cards):
    if calculate_score(cards)> 21:
        return True
    return False


def check_host(host_card):
    return False if calculate_score(host_card) >= 17 else True


def check_blackjack(picked_card):
    blackjack = False
    if "A" in picked_card:
        a_count = 0
        for card in picked_card:

            if a_count > 1:
                blackjack = False
                break

            if card in ['J', 'Q', 'K', 'A']:
                blackjack = True
                if card == 'A':
                    a_count += 1
            else:
                blackjack = False
                break
    return blackjack
