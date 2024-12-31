import colorama
import os
import sys
import random
from time import sleep
from colorama import Fore, Style
from collections import deque, defaultdict

from MinimaxAlphaBeta import FindBestMove, MAX_DEPTH
from utility import check_win, WIN_CONDITIONS

colorama.init(autoreset=True)

random_colour = [Fore.BLUE, Fore.LIGHTBLUE_EX, Fore.CYAN, Fore.LIGHTCYAN_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.LIGHTYELLOW_EX, Fore.YELLOW]

result_counter_single = defaultdict(lambda: defaultdict(int, {'wins': 0, 'losses': 0, 'draws': 0}))
result_counter_multi = defaultdict(lambda: defaultdict(int, {'wins': 0, 'draws': 0}))

played_single = False
played_multi = False

RED_DISC = Fore.RED + "O"
YELLOW_DISC = Fore.YELLOW + "O"

def clear_screen():
    if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
        os.system('clear')
    elif sys.platform.startswith('win32'):
        os.system('cls')

def welcome_screen():
    clear_screen()
    print(Fore.YELLOW + Style.BRIGHT + '\033[4m' + "Welcome to Connect Four!" + '\033[24m')
    sleep(1.5)

def game_mode():
    while True:
        try:
            sleep(0.4)
            print(Fore.CYAN + "Choose Your Game Mode!\n")
            sleep(0.8)
            print(Fore.LIGHTYELLOW_EX + "1. Single Player (Vs Computer)")
            sleep(0.4)
            print(Fore.LIGHTMAGENTA_EX + "2. Two Player Mode\n")
            sleep(1)
            choice = input(Fore.LIGHTWHITE_EX + "Enter 1 or 2: ").strip()
            print()
            clear_screen()

            if choice == "1":
                print(Fore.LIGHTYELLOW_EX + "Starting Single Player Mode!\n")
                sleep(0.7)
                print()
                return "single"

            elif choice == "2":
                print(Fore.LIGHTMAGENTA_EX + "Starting Two Player Mode!")
                sleep(0.7)
                print()
                return "multi"

            else:
                raise ValueError(Fore.LIGHTRED_EX + "Invalid choice! Please enter 1 or 2 only.")
        except ValueError as error:
            print(error)

def initialise_board():
    return [deque([' '] * 6) for _ in range(7)]

def check_draw(board):
    return all(board[col][0] != ' ' for col in range(7))

def display_board(board):
    clear_screen()

    for row in range(6):
        row_string = ""
        for col in range(7):
            row_string += Fore.CYAN + "| " + board[col][row] + " "
        row_string += "|"
        print(row_string)
        print(Fore.GREEN + "------------------------------" + Fore.RESET)


def player_move(board, player_disc, player_number):
    disc_colour = Fore.RED if player_disc == RED_DISC else Fore.YELLOW
    while True:
        try:
            sleep(0.2)
            col = int(input(disc_colour + "Enter a column (1-7): ")) - 1
            if 0 <= col < 7 and board[col][0] == ' ':
                for row in reversed(range(6)):
                    if board[col][row] == ' ':
                        board[col][row] = player_disc
                        display_board(board)
                        # Check for win
                        if check_win(board, WIN_CONDITIONS, player_disc):
                            print(Fore.GREEN + f"Player {player_number} wins!")
                            return True
                        # Check for draw
                        if check_draw(board):
                            print(Fore.LIGHTWHITE_EX + "It's a draw!")
                            return True
                        return False
            else:
                print(Fore.RED + "Column is full or invalid, try again.")
        except ValueError:
            print(Fore.RED + "Invalid input, please enter a number (1-7).")

def computer_minimax_move(board, player, computer):
    best_col = FindBestMove(board, player, computer)
    for row in reversed(range(6)):
        if board[best_col][row] == ' ':
            board[best_col][row] = computer
            disc_symbol = "🔴" if computer == RED_DISC else "🟡"
            disc_colour = Fore.RED if computer == RED_DISC else Fore.YELLOW
            print()
            print(f"{disc_colour}Computer placed disc ({disc_symbol}) in column {best_col + 1}")
            sleep(0.7)
            break
    # Check for win
    if check_win(board, WIN_CONDITIONS, computer):
        display_board(board)
        print(Fore.GREEN + "Computer wins!")
        return True
    return False

def disc_colour(mode):
    if mode == "multi":
        while True:
            try:
                clear_screen()
                print(Fore.LIGHTYELLOW_EX + "Choose Your " + Fore.LIGHTRED_EX + "Disc Colour!\n")
                print(Fore.RED + "1. Red (🔴)")
                print(Fore.YELLOW + "2. Yellow (🟡)\n")
                disc_colour = int(input("Enter 1 or 2: ").strip())

                if disc_colour == 1:
                    player1 = RED_DISC
                    player2 = YELLOW_DISC
                    sleep(0.5)
                    return player1, player2

                elif disc_colour == 2:
                    player1 = YELLOW_DISC
                    player2 = RED_DISC
                    sleep(0.5)
                    return player1, player2

                else:
                    raise ValueError(Fore.LIGHTRED_EX + "Invalid Choice, Please Choose 1 or 2 Only")
            except ValueError as error:
                print(error)

    elif mode == "single":
        while True:
            try:
                print(Fore.LIGHTYELLOW_EX + "Choose Your " + Fore.LIGHTRED_EX + "Disc Colour!\n")
                print(Fore.RED + "1. Red (🔴)")
                print(Fore.YELLOW + "2. Yellow (🟡)\n")
                disc_colour = int(input("Enter 1 or 2: ").strip())

                if disc_colour == 1:
                    player = RED_DISC
                    computer = YELLOW_DISC
                    return player, computer

                elif disc_colour == 2:
                    player = YELLOW_DISC
                    computer = RED_DISC
                    return player, computer

                else:
                    raise ValueError(Fore.LIGHTRED_EX + "Invalid Choice, Please Choose 1 or 2 Only")
            except ValueError as error:
                print(error)

def game_loop(board, win_conditions, mode, player1=None, player2=None, player=None, computer=None):
    if mode == "multi":
        current_player = player1
        player_number = 1
    elif mode == "single":
        current_player = player  # Start with the human player
        player_number = 1

    moves_counter = defaultdict(int)
    turn_counter = defaultdict(int)

    while moves_counter['total'] < 42:
        display_board(board)

        turn_counter['turn'] += 1
        print(random.choice(random_colour) + Style.BRIGHT + f"Turn {turn_counter['turn']}")
        print()

        if check_win(board, win_conditions, current_player):
            handle_win(board, mode, current_player, player1, player2, player, computer)
            break

        if mode == "multi":
            if player_move(board, current_player, player_number):
                break
            current_player = player2 if current_player == player1 else player1
            player_number = 2 if player_number == 1 else 1
        elif mode == "single":
            if current_player == player:
                if player_move(board, player, player_number):
                    break
                current_player = computer
                player_number = 2
            else:
                print(Fore.YELLOW + "Computer is thinking...")
                sleep(1)
                if computer_minimax_move(board, player, computer):
                    break
                current_player = player
                player_number = 1

        moves_counter['total'] += 1

        # Check for draw after each move
        if check_draw(board):
            handle_draw(board, mode)
            break

def handle_win(board, mode, current_player, player1, player2, player, computer):
    display_board(board)
    if mode == "multi":
        if current_player == player1:
            winner = "Player 1"
            result_counter_multi['player1']['wins'] += 1
        elif current_player == player2:
            winner = "Player 2"
            result_counter_multi['player2']['wins'] += 1
    elif mode == "single":
        if current_player == player:
            winner = "You"
            result_counter_single['single']['wins'] += 1
        elif current_player == computer:
            winner = "Computer"
            result_counter_single['single']['losses'] += 1

    if winner == "You":
        print(Fore.LIGHTGREEN_EX + f"{winner} win!")
    else:
        print(Fore.LIGHTGREEN_EX + f"{winner} wins!")

def switch_player(mode, current_player, player1, player2, player, computer, moves_counter, board):
    if moves_counter['total'] == 42:
        handle_draw(board, mode)
        return None
    if mode == "multi":
        return player2 if current_player == player1 else player1
    elif mode == "single":
        return computer if current_player == player else player

def handle_draw(board, mode):
    global played_single, played_multi
    display_board(board)
    print(Fore.LIGHTCYAN_EX + "It's a Draw!")
    if mode == "multi":
        result_counter_multi['player1']['draws'] += 1
        result_counter_multi['player2']['draws'] += 1
        played_multi = False
    elif mode == "single":
        result_counter_single['single']['draws'] += 1
        played_single = False

def handle_play_again(mode, result_counter_single, result_counter_multi):
    while True:
        try:
            play_again = input("Do you want to play again? (yes/no): ").strip().lower()
            if play_again == "yes" or play_again == "y":
                main()
            elif play_again == "no" or play_again == "n":
                print("\n" + Style.BRIGHT + Fore.LIGHTRED_EX + "Game " + Fore.LIGHTYELLOW_EX + "Results:\n")

                if played_multi:
                    print(f"{random.choice(random_colour)}Player 1 - {Fore.LIGHTGREEN_EX}Wins: {result_counter_multi['player1']['wins']} | "
                          f"{Fore.LIGHTYELLOW_EX}Draws: {result_counter_multi['player1']['draws']}")

                    print(f"{random.choice(random_colour)}Player 2 - {Fore.LIGHTGREEN_EX}Wins: {result_counter_multi['player2']['wins']} | "
                          f"{Fore.LIGHTYELLOW_EX}Draws: {result_counter_multi['player2']['draws']}")

                if played_single:
                    print(f"{random.choice(random_colour)}You - {Fore.LIGHTGREEN_EX}Wins: {result_counter_single['single']['wins']} | "
                          f"{Fore.LIGHTYELLOW_EX}Losses: {result_counter_single['single']['losses']} | "
                          f"{Fore.LIGHTRED_EX}Draws: {result_counter_single['single']['draws']}")

                    print()

                    print(f"{random.choice(random_colour)}Computer - {Fore.LIGHTGREEN_EX}Wins: {result_counter_single['single']['wins']} | "
                          f"{Fore.LIGHTYELLOW_EX}Losses: {result_counter_single['single']['losses']} | "
                          f"{Fore.LIGHTRED_EX}Draws: {result_counter_single['single']['draws']}")

                sleep(5)
                print(Fore.LIGHTBLUE_EX + "\n" + "Thanks for playing!")
                sys.exit()

            else:
                raise ValueError(Fore.LIGHTRED_EX + "Invalid input! Please enter 'yes' or 'no' only.")
        except ValueError as error:
            print(error)

def main():
    global played_single, played_multi
    welcome_screen()
    board = initialise_board()
    display_board(board)

    mode = game_mode()

    if mode == "single":
        played_single = True
    elif mode == "multi":
        played_multi = True

    if mode == "multi":
        player1, player2 = disc_colour(mode)
        game_loop(board, WIN_CONDITIONS, mode, player1=player1, player2=player2)
    elif mode == "single":
        player, computer = disc_colour(mode)
        game_loop(board, WIN_CONDITIONS, mode, player=player, computer=computer)

    handle_play_again(mode, result_counter_single, result_counter_multi)

if __name__ == "__main__":
    main()
