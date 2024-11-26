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


def get_card_value(card):
    value = VALUES.index(card[0])  # Индекс значения (A=0, 2=1, ..., 8=7)
    suit = SUITS.index(card[1])    # Индекс масти (C=0, D=1, H=2, S=3)
    return value * 4 + suit        # Уникальное значение карты


def play_round(hands, round_number):
    print(f"\nTRICK #{round_number + 1}")
    played_cards = {}

    for player, cards in hands.items():
        if "Computer" in player:
            # Ход компьютера (выбирает первую доступную карту)
            chosen_card = cards.pop(0)
            print(f"{player} played: {chosen_card}")
        else:
            # Ход игрока
            while True:
                print(f"{player}, your cards: {', '.join(cards)}")
                chosen_card = input("Choose a card to play (e.g., 'A C'): ").upper()
                if chosen_card in cards:
                    cards.remove(chosen_card)
                    break
                print("Invalid card. Try again.")
            print(f"{player} played: {chosen_card}")

        played_cards[player] = chosen_card

    winner = max(played_cards, key=lambda p: get_card_value(played_cards[p]))
    print(f"{winner} wins the trick with {played_cards[winner]}!")
    return winner


def start_game():
    deck = generate_deck()
    shuffle_deck(deck)
    num_players = 2  # TODO: сделать ввод количества игроков
    hands = deal_cards(deck, num_players)

    print("\nSTARTING THE GAME...")
    display_hands(hands)

    scores = {player: 0 for player in hands}

    for round_number in range(8):
        winner = play_round(hands, round_number)
        scores[winner] += 1  # Победитель получает 1 очко

    final_winner = max(scores, key=scores.get)
    print("\nFINAL SCORES:")
    for player, score in scores.items():
        print(f"{player}: {score} points")
    print(f"\n{final_winner} wins the game! Congratulations!")
