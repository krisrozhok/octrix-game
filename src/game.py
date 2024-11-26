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
    players = list(hands.keys())
    print(f"\n{players[0].upper()}'S HAND".ljust(20) + f"{players[1].upper()}'S HAND")
    print("CLB    DIA    HRT    SPD".ljust(20) + "CLB    DIA    HRT    SPD")
    for i in range(8):  # 8 строк для каждой карты
        row = ""
        for player in players:
            card = hands[player][i]
            row += f"! {card} " if card else "! *  "
        print(row + "!")



def get_card_input(player_name, available_cards):
    while True:
        card = input(f"WHAT CARD, {player_name.upper()}? ").strip().upper()
        if card in available_cards:
            return card
        print("BAD INPUT, RE-ENTER")


def display_round_results(round_number, played_cards, winner):
    print(f"\nTRICK # {round_number + 1} (HIGH CARD WINS)")
    for player, card in played_cards.items():
        print(f"{player.upper()} PLAYED {card}")
    print(f"{winner.upper()} WON TRICK # {round_number + 1}")


def get_card_value(card):
    value = VALUES.index(card[0])  # Индекс значения (A=0, 2=1, ..., 8=7)
    suit = SUITS.index(card[1])    # Индекс масти (C=0, D=1, H=2, S=3)
    return value * 4 + suit        # Уникальное значение карты

def display_final_scores(scores):
    print("\nFINAL SCORES:")
    for player, score in scores.items():
        print(f"{player.upper()}: {score} POINTS")
    winner = max(scores, key=scores.get)
    print(f"\n{winner.upper()} WON THE GAME, CONGRATULATIONS!")


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
    num_players = 2  # Игрок против компьютера
    hands = deal_cards(deck, num_players)

    display_hands(hands)

    scores = {player: 0 for player in hands}
    for round_number in range(8):
        played_cards = {}
        for player, cards in hands.items():
            if "COMPUTER" in player.upper():
                chosen_card = cards.pop(0)
            else:
                chosen_card = get_card_input(player, cards)
                cards.remove(chosen_card)
            played_cards[player] = chosen_card
        winner = max(played_cards, key=lambda p: get_card_value(played_cards[p]))
        scores[winner] += 1
        display_round_results(round_number, played_cards, winner)
    display_final_scores(scores)
