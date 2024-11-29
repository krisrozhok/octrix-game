from main import (
    SUITS, VALUES, SUIT_NAMES, VALUE_NAMES,
    format_card, parse_card_input, calculate_score,
    POINTS_STANDARD, MAX_PLAYERS
)
import random


class GameAdapter:
    def __init__(self, socketio, session_id):
        self.socketio = socketio
        self.session_id = session_id
        self.state = 'init'
        self.game_state = {
            'players': [],
            'hands': {},
            'scores': {},
            'points_limit': POINTS_STANDARD,
            'current_round': 1,
            'high_wins': True,
            'trick_winners': [],
            'played_cards': {},
            'waiting_for_input': False,
            'current_player': None
        }

    def emit_to_client(self, event, data):
        self.socketio.emit(event, data, room=self.session_id)

    def handle_input(self, input_text):
        input_text = input_text.strip().upper()

        if self.state == 'init':
            if not hasattr(self, 'teach_shown'):
                if input_text.startswith('Y'):
                    self.teach_game()
                self.teach_shown = True
                self.emit_to_client('input_request', 'HOW MANY POINTS (0 ENTRY GIVES STANDARD 88)? ')
                return
            else:
                try:
                    self.game_state['points_limit'] = POINTS_STANDARD if not input_text or input_text == "0" else int(
                        input_text)
                    self.state = 'get_players'
                    self.emit_to_client('input_request', 'HOW MANY PLAYERS? ')
                except ValueError:
                    self.emit_to_client('output', "Invalid input. Please enter a number.\n")
                    self.emit_to_client('input_request', 'HOW MANY POINTS (0 ENTRY GIVES STANDARD 88)? ')
                return

        elif self.state == 'get_players':
            if not hasattr(self, 'num_players'):
                try:
                    num = int(input_text)
                    if 1 <= num <= MAX_PLAYERS:
                        self.num_players = num
                        self.players_added = 0
                        self.emit_to_client('input_request', "ENTER PLAYER'S NAME? ")
                    else:
                        self.emit_to_client('output', "ONLY ONE TO FOUR PLAYERS ALLOWED, RE-ENTER\n")
                        self.emit_to_client('input_request', 'HOW MANY PLAYERS? ')
                except ValueError:
                    self.emit_to_client('output', "ONLY ONE TO FOUR PLAYERS ALLOWED, RE-ENTER\n")
                    self.emit_to_client('input_request', 'HOW MANY PLAYERS? ')
                return

            if self.players_added < self.num_players:
                if input_text and not input_text.startswith(' '):
                    self.game_state['players'].append(input_text)
                    self.players_added += 1
                    if self.players_added < self.num_players:
                        self.emit_to_client('input_request', "ENTER PLAYER'S NAME? ")
                    else:
                        if self.num_players < MAX_PLAYERS:
                            self.emit_to_client('input_request', "SHOULD I PLAY TOO(Y OR N)? ")
                        else:
                            self.start_game()
                else:
                    self.emit_to_client('output', "DON'T START NAME WITH SPACE, RE-\n")
                    self.emit_to_client('input_request', "ENTER PLAYER'S NAME? ")
                return

            if not hasattr(self, 'computer_asked') and self.num_players < MAX_PLAYERS:
                self.computer_asked = True
                if input_text.startswith('Y'):
                    self.game_state['players'].append('COMPUTER')
                self.start_game()
                return

        elif self.state == 'playing':
            self.handle_game_input(input_text)

    def handle_game_input(self, input_text):
        current_player = self.game_state['current_player']

        if input_text.upper() == 'P':
            self.display_hands()
            self.emit_to_client('input_request', "? ")
            return

        card = parse_card_input(input_text, self.game_state['hands'][current_player])
        if card is None:
            self.emit_to_client('output', "BAD INPUT, RE-ENTER\n")
            self.emit_to_client('input_request', "? ")
            return

        self.play_card(current_player, card)

    def play_card(self, player, card):
        self.game_state['hands'][player].remove(card)
        self.game_state['played_cards'][player] = card
        self.emit_to_client('output', f"{player} PLAYED THE {format_card(card)}\n")

        # Проверяем, все ли игроки сделали ход
        if len(self.game_state['played_cards']) == len(self.game_state['players']):
            self.resolve_trick()
        else:
            next_player_index = (self.game_state['players'].index(player) + 1) % len(self.game_state['players'])
            self.game_state['current_player'] = self.game_state['players'][next_player_index]
            if self.game_state['current_player'] == 'COMPUTER':
                self.play_computer_card()
            else:
                self.emit_to_client('output', f"WHAT CARD, {self.game_state['current_player']}\n")
                self.emit_to_client('input_request', "? ")

    def play_computer_card(self):
        cards = self.game_state['hands']['COMPUTER']
        if self.game_state['high_wins']:
            card = max(cards, key=lambda x: x[0] * 4 + x[1])
        else:
            card = min(cards, key=lambda x: x[0] * 4 + x[1])
        self.play_card('COMPUTER', card)

    def resolve_trick(self):
        played_cards = self.game_state['played_cards']
        high_wins = self.game_state['high_wins']

        winner = max(played_cards.items(), key=lambda x: x[1][0] * 4 + x[1][1]) if high_wins else \
            min(played_cards.items(), key=lambda x: x[1][0] * 4 + x[1][1])

        self.game_state['trick_winners'].append(winner[0])
        self.emit_to_client('output', f"{winner[0]} WON TRICK # {self.game_state['current_round']}\n")

        # Подготовка к следующему трику или окончание раунда
        if self.game_state['current_round'] < 8:
            self.prepare_next_trick()
        else:
            self.end_round()

    def prepare_next_trick(self):
        played_cards = self.game_state['played_cards']
        high_card = max(played_cards.values(), key=lambda x: x[0] * 4 + x[1])
        low_card = min(played_cards.values(), key=lambda x: x[0] * 4 + x[1])
        self.game_state['high_wins'] = (high_card[1] % 2) == (low_card[1] % 2)

        self.game_state['current_round'] += 1
        self.game_state['played_cards'] = {}
        self.start_trick()

    def end_round(self):
        # Подсчет очков
        for player in self.game_state['players']:
            player_tricks = [winner == player for winner in self.game_state['trick_winners']]
            score = calculate_score(player_tricks)
            self.game_state['scores'][player] += score
            self.emit_to_client('output',
                                f"{player} SCORED {score} POINTS AND NOW HAS {self.game_state['scores'][player]}\n")

        if max(self.game_state['scores'].values()) >= self.game_state['points_limit']:
            winner = max(self.game_state['scores'].items(), key=lambda x: x[1])[0]
            self.emit_to_client('output', f"\n{winner} WON THE GAME!\n")
            self.emit_to_client('input_request', "\nANOTHER GAME(Y OR N)? ")
            self.state = 'game_end'
        else:
            self.start_round()

    def start_game(self):
        self.state = 'playing'
        self.game_state['scores'] = {player: 0 for player in self.game_state['players']}
        self.start_round()

    def start_round(self):
        deck = [(value, suit) for value in range(8) for suit in range(4)]
        random.shuffle(deck)
        self.game_state['hands'] = {player: [] for player in self.game_state['players']}

        for _ in range(8):
            for player in self.game_state['players']:
                if deck:
                    self.game_state['hands'][player].append(deck.pop())

        self.display_hands()
        self.game_state['current_round'] = 1
        self.game_state['trick_winners'] = []
        self.game_state['high_wins'] = True
        self.game_state['played_cards'] = {}
        self.start_trick()

    def start_trick(self):
        self.emit_to_client('output', f"\nTRICK # {self.game_state['current_round']} "
                                      f"({'HIGH' if self.game_state['high_wins'] else 'LOW'} CARD WINS)\n")
        self.game_state['current_player'] = self.game_state['players'][0]
        if self.game_state['current_player'] == 'COMPUTER':
            self.play_computer_card()
        else:
            self.emit_to_client('output', f"WHAT CARD, {self.game_state['current_player']}\n")
            self.emit_to_client('input_request', "? ")

    def display_hands(self):
        output = "\n"
        visible_hands = {p: h for p, h in self.game_state['hands'].items() if p != 'COMPUTER'}

        for i, player in enumerate(visible_hands):
            name_width = 35  # Ширина колонки для руки
            player_text = f"{player}'S HAND:"
            padding = (name_width - len(player_text)) // 2

            if i > 0:
                output += " " * 5

            output += " " * padding + player_text + " " * (name_width - len(player_text) - padding)
        output += "\n"

        for player in visible_hands:
            output += "         CLB    DIA    HRT    SPD"
            if len(visible_hands) > 1:
                output += " " * 5
        output += "\n"

        for value_idx, value in enumerate(VALUES):
            line = ""
            for player in visible_hands:
                current_line = f"!{value}     "
                for suit in SUITS:
                    card = (value_idx, SUITS.index(suit))
                    if card in visible_hands[player]:
                        current_line += "!*     "
                    else:
                        current_line += "!      "
                current_line += f"!{value}"
                if len(visible_hands) > 1 and player != list(visible_hands.keys())[-1]:
                    current_line += " " * 5
                line += current_line
            output += line + "\n"

        self.emit_to_client('output', output)

    def teach_game(self):
        instructions = """  THIS IS A GAME CALLED OCTRIX.  EACH PLAYER IS DEALT 8
CARDS RANGING FROM ACE THROUGH EIGHT.  THE CARDS ARE
RANKED ACCORDING TO BRIDGE SUITS WITH THE ACE OF CLUBS THE
LOWEST AND THE EIGHT OF SPADES HIGHEST.  THE OBJECT IS TO
WIN AS MANY OF THE EIGHT TRICKS AS POSSIBLE.  EACH TRICK
PLAYED DETERMINES THE PLAY OF THE NEXT TRICK.  IF THE HIGH
AND LOW CARDS PLAYED MATCH COLOR THE NEXT TRICK WILL BE
HIGH AND IF THEY DO NOT MATCH IT WILL BE LOW.  IT IS IM-
PORTANT TO SET STRATEGY TO WIN CONSECUTIVE TRICKS IN THAT
SCORING IS 1 POINT PER TRICK, 4 FOR TWO IN A ROW,9 FOR 3, UP
TO 64 FOR ALL EIGHT.

    RESPOND TO THE INPUT PROMPT WITH THE CARD YOU WANT TO
PLAY IN A TWO CHARACTER FORMAT WITH THE VALUE(A-8) AS THE
FIRST CHARACTER, AND SUIT(C,D,H,S) AS THE SECOND CHARACTER.
    (TO SEE THE REMAINING CARDS, ENTER A'P' IN
    RESPONSE TO THE 'WHAT CARD' QUERY)

THAT'S IT, GOOD LUCK!!
"""
        self.emit_to_client('output', instructions + "\n")
