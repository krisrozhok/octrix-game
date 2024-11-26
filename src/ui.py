def print_tab(text, tab_position):
    print(" " * tab_position + text)


def display_title():
    print("\n" * 2)
    print_tab("OCTRIX", 27)
    print_tab("CREATIVE COMPUTING", 20)
    print_tab("MORRISTOWN, NEW JERSEY", 18)
    print("\n" * 2)


def teach_game():
    print("TEACH GAME (Y OR N)?", end=" ")
    choice = input().strip().upper()
    if choice == "Y":
        print("\nTHIS IS A GAME CALLED OCTRIX.")
        print("EACH PLAYER IS DEALT 8 CARDS RANGING FROM ACE THROUGH EIGHT.")
        print("THE CARDS ARE RANKED ACCORDING TO BRIDGE SUITS WITH THE")
        print("ACE OF CLUBS THE LOWEST AND THE EIGHT OF SPADES HIGHEST.")
        print("THE OBJECT IS TO WIN AS MANY OF THE EIGHT TRICKS AS POSSIBLE.")
        print("SCORING IS 1 POINT PER TRICK, 4 FOR TWO IN A ROW, 9 FOR THREE,")
        print("UP TO 64 FOR ALL EIGHT.")
        print("\nRESPOND TO THE INPUT PROMPT WITH THE CARD YOU WANT TO PLAY")
        print("IN A TWO CHARACTER FORMAT WITH THE VALUE (A-8) AS THE FIRST")
        print("CHARACTER AND THE SUIT (C, D, H, S) AS THE SECOND CHARACTER.")
        print("\nTO SEE THE REMAINING CARDS, ENTER 'P' IN RESPONSE TO THE")
        print("'WHAT CARD' QUERY.")
        print("\nTHAT'S IT, GOOD LUCK!!")
