import random


def print_centered(text, width=72):
    """Вывод строки по центру."""
    print(text.center(width))


def print_tabbed(text, tab=0):
    """Вывод строки с отступом."""
    print(" " * tab + text)


def initialize_game():
    """Инициализация игры Octrix."""
    print_tabbed("OCTRIX", 27)
    print_tabbed("CREATIVE COMPUTING", 20)
    print_tabbed("MORRISTOWN, NEW JERSEY", 18)
    print("\n" * 2)
    print("Welcome to Octrix!")
    print("Each player is dealt 8 cards ranging from Ace through Eight.")
    print("The objective is to win as many tricks as possible.")
    print("\n" * 2)


def create_deck():
    """Создаем колоду карт."""
    suits = ["C", "D", "H", "S"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8"]
    return [r + s for r in ranks for s in suits]


def deal_cards(deck, num_players=4):
    """Раздаем карты игрокам."""
    random.shuffle(deck)
    hands = [deck[i::num_players] for i in range(num_players)]
    return hands


if __name__ == "__main__":
    initialize_game()
    deck = create_deck()
    hands = deal_cards(deck, 4)
    for i, hand in enumerate(hands):
        print(f"Player {i + 1} cards: {', '.join(hand)}")