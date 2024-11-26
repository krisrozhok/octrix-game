import random

VALUES = ["A", "2", "3", "4", "5", "6", "7", "8"]
SUITS = ["C", "D", "H", "S"]


def generate_deck():
    return [value + suit for value in VALUES for suit in SUITS]


def shuffle_deck(deck):
    random.shuffle(deck)


def deal_cards(deck, num_players):
    hands = {f"Player {i+1}": [] for i in range(num_players)}
    for _ in range(8):  # Каждому игроку по 8 карт
        for player in hands:
            hands[player].append(deck.pop(0))
    return hands


def display_hands(hands):
    print("\n" + " " * 9 + "CLB    DIA    HRT    SPD")
    for i in range(8):  # По 8 карт на игрока
        row = ""
        for player, cards in hands.items():
            card = cards[i]
            row += f"!  {card}  "
        print(row + "!")


def start_game():
    deck = generate_deck()
    shuffle_deck(deck)
    num_players = 2  # TODO: сделать ввод количества игроков
    hands = deal_cards(deck, num_players)
    print("\nSTARTING THE GAME...")
    display_hands(hands)
