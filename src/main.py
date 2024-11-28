import random

SUITS = ["CLB", "DIA", "HRT", "SPD"]
SUIT_NAMES = ["CLUBS", "DIAMONDS", "HEARTS", "SPADES"]
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8"]
VALUE_NAMES = ["ACE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT"]
POINTS_STANDARD = 88
MAX_PLAYERS = 4


def print_title():
    print(" " * 27 + "OCTRIX")
    print(" " * 20 + "CREATIVE COMPUTING")
    print(" " * 18 + "MORRISTOWN, NEW JERSEY")
    print("\n" * 3)


def teach_game():
    print("  THIS IS A GAME CALLED OCTRIX.  EACH PLAYER IS DEALT 8")
    print("CARDS RANGING FROM ACE THROUGH EIGHT.  THE CARDS ARE")
    print("RANKED ACCORDING TO BRIDGE SUITS WITH THE ACE OF CLUBS THE")
    print("LOWEST AND THE EIGHT OF SPADES HIGHEST.  THE OBJECT IS TO")
    print("WIN AS MANY OF THE EIGHT TRICKS AS POSSIBLE.  EACH TRICK")
    print("PLAYED DETERMINES THE PLAY OF THE NEXT TRICK.  IF THE HIGH")
    print("AND LOW CARDS PLAYED MATCH COLOR THE NEXT TRICK WILL BE")
    print("HIGH AND IF THEY DO NOT MATCH IT WILL BE LOW.  IT IS IM-")
    print("PORTANT TO SET STRATEGY TO WIN CONSECUTIVE TRICKS IN THAT")
    print("SCORING IS 1 POINT PER TRICK, 4 FOR TWO IN A ROW,9 FOR 3, UP")
    print("TO 64 FOR ALL EIGHT.")
    print()
    print("    RESPOND TO THE INPUT PROMPT WITH THE CARD YOU WANT TO")
    print("PLAY IN A TWO CHARACTER FORMAT WITH THE VALUE(A-8) AS THE")
    print("FIRST CHARACTER, AND SUIT(C,D,H,S) AS THE SECOND CHARACTER.")
    print("    (TO SEE THE REMAINING CARDS, ENTER A'P' IN")
    print("    RESPONSE TO THE 'WHAT CARD' QUERY)")
    print()
    print("THAT'S IT, GOOD LUCK!!")


def display_hands(hands):
    COLUMN_WIDTH = 35

    for player in hands:
        if player != "COMPUTER":
            name_with_hand = f"{player}'S HAND"
            total_spaces = COLUMN_WIDTH - len(name_with_hand)
            left_spaces = total_spaces // 2
            right_spaces = total_spaces - left_spaces
            centered_text = " " * left_spaces + name_with_hand + " " * right_spaces
            print(centered_text, end="")
    print()

    for player in hands:
        if player != "COMPUTER":
            # Центрируем названия мастей в колонке
            print("         CLB    DIA    HRT    SPD", end="")
    print()

    for value_idx, value in enumerate(VALUES):
        for player in hands:
            if player == "COMPUTER":
                continue
            line = f"!{value}     "
            for suit in SUITS:
                card = (value_idx, SUITS.index(suit))
                if card in hands[player]:
                    line += "!*     "
                else:
                    line += "!      "
            print(line[:-1], end="")
        print(f"!{value}")
    print()


def initialize_game():
    while True:
        try:
            num_players = int(input("HOW MANY PLAYERS? ").strip())
            if 1 <= num_players <= MAX_PLAYERS:
                break
            print("ONLY ONE TO FOUR PLAYERS ALLOWED, RE-ENTER")
        except ValueError:
            print("ONLY ONE TO FOUR PLAYERS ALLOWED, RE-ENTER")

    players = []
    for i in range(num_players):
        while True:
            name = input("ENTER PLAYER'S NAME? ").strip().upper()
            if name and not name.startswith(" "):
                players.append(name)
                break
            print("DON'T START NAME WITH SPACE, RE-")

    if num_players < MAX_PLAYERS and num_players == 1 or (
        num_players < 4 and
        input("SHOULD I PLAY TOO(Y OR N)? ").strip().upper().startswith("Y")
    ):
        players.append("COMPUTER")

    return players



def generate_deck():
    deck = [(value, suit) for value in range(8) for suit in range(4)]
    random.shuffle(deck)
    return deck


def deal_cards(deck, players):
    hands = {player: [] for player in players}
    for i in range(8):
        for player in players:
            if deck:
                hands[player].append(deck.pop())
    return hands


def computer_play(cards, high_wins):
    if high_wins:
        return max(cards, key=lambda x: x[0] * 4 + x[1])
    return min(cards, key=lambda x: x[0] * 4 + x[1])


def format_card(card):
    value, suit = card
    return f"{VALUE_NAMES[value]} OF {SUIT_NAMES[suit]}"


def parse_card_input(card_input, hand):
    if len(card_input) != 2:
        return None

    card_input = card_input.upper()
    value, suit = card_input[0], card_input[1]

    try:
        if value == "A":
            value_idx = 0
        else:
            value_idx = int(value) - 1
            if not (0 <= value_idx <= 7):
                return None
    except ValueError:
        return None

    suit_map = {"C": 0, "D": 1, "H": 2, "S": 3}
    if suit not in suit_map:
        return None
    suit_idx = suit_map[suit]

    card = (value_idx, suit_idx)
    if card not in hand:
        return None

    return card


def play_round(hands, round_num, high_wins=True):
    print(f"\nTRICK # {round_num} ({'HIGH' if high_wins else 'LOW'} CARD WINS)")
    played_cards = {}

    for player in hands:
        while True:
            if player != "COMPUTER":
                print(f"WHAT CARD, {player}")
            if player == "COMPUTER":
                card = computer_play(hands[player], high_wins)
                print(f"I PLAYED THE {format_card(card)}")
                break
            else:
                card_input = input("? ").strip()
                if card_input.upper() == "P":
                    display_hands({p: h for p, h in hands.items() if p != "COMPUTER"})
                    continue

                card = parse_card_input(card_input, hands[player])
                if card is None:
                    print("BAD INPUT, RE-ENTER")
                    continue

                print(f"{player} PLAYED THE {format_card(card)}")
                break

        hands[player].remove(card)
        played_cards[player] = card

    winner = max(played_cards.items(), key=lambda x: x[1][0] * 4 + x[1][1]) if high_wins else \
        min(played_cards.items(), key=lambda x: x[1][0] * 4 + x[1][1])

    print(f"{winner[0]} WON TRICK # {round_num}")
    return winner[0]


def calculate_score(tricks_won):
    score = 0
    streak = 0
    for won in tricks_won:
        if won:
            streak += 1
        else:
            if streak > 0:
                score += streak * streak
            streak = 0
    if streak > 0:
        score += streak * streak
    return score


def main():
    print_title()

    if input("TEACH GAME(Y OR N)? ").strip().upper().startswith("Y"):
        teach_game()

    while True:
        points_input = input("HOW MANY POINTS (0 ENTRY GIVES STANDARD 88)? ").strip()
        points_limit = POINTS_STANDARD if not points_input or points_input == "0" else int(points_input)

        players = initialize_game()
        scores = {player: 0 for player in players}

        while max(scores.values()) < points_limit:
            deck = generate_deck()
            hands = deal_cards(deck, players)
            display_hands({p: h for p, h in hands.items() if p != "COMPUTER"})

            trick_winners = []
            high_wins = True

            for round_num in range(1, 9):
                winner = play_round(hands, round_num, high_wins)
                trick_winners.append(winner)

                if round_num < 8:
                    played_cards = []
                    for player_hand in hands.values():
                        played_cards.extend(player_hand)
                    high_card = max(played_cards, key=lambda x: x[0] * 4 + x[1])
                    low_card = min(played_cards, key=lambda x: x[0] * 4 + x[1])
                    high_wins = (high_card[1] % 2) == (low_card[1] % 2)

            for player in players:
                player_tricks = [winner == player for winner in trick_winners]
                score = calculate_score(player_tricks)
                scores[player] += score
                print(f"{player} SCORED {score} POINTS AND NOW HAS {scores[player]}")

        winner = max(scores.items(), key=lambda x: x[1])[0]
        print(f"\n{winner} WON THE GAME!")

        if input("\nANOTHER GAME(Y OR N)? ").strip().upper().startswith("N"):
            break


if __name__ == "__main__":
    main()
