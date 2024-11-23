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

if __name__ == "__main__":
    initialize_game()
