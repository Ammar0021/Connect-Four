from MinimaxAlphaBeta import *
import colorama
import os
import sys
import random
from random import randint
from time import sleep
from colorama import Fore, Style
from collections import deque, defaultdict


colorama.init(autoreset=True)

random_colour = [Fore.BLUE, Fore.LIGHTBLUE_EX, Fore.CYAN, Fore.LIGHTCYAN_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX,Fore.LIGHTYELLOW_EX, Fore.YELLOW]

result_counter_single = defaultdict(lambda: defaultdict(int, {'wins': 0, 'losses': 0, 'draws': 0}))
result_counter_multi = defaultdict(lambda: defaultdict(int, {'wins': 0, 'draws': 0}))

played_single = False
played_multi = False


RED_DISC = Fore.RED + "O"
YELLOW_DISC = Fore.YELLOW + "O"


def clear_screen():  
    if sys.platform.startswith('darwin'):
        os.system('clear')
    elif sys.platform.startswith('linux'):
        os.system('clear')  
    elif sys.platform.startswith('win32'):
        os.system('cls') 

def welcome_screen():
    clear_screen()
    print(Fore.YELLOW + Style.BRIGHT + '\033[4m' + "Welcome to Connect Four!" + '\033[24m')
    sleep(2)
    
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
    return [deque([' '] * 6) for i in range(7)]

def display_board(board):
    clear_screen()

    for row in range(6):  
        row_string = ""
        
        for col in range(7):
            row_string += Fore.CYAN + "| " + board[col][row] + " "
        row_string += "|"
        print(row_string)
        print(Fore.GREEN + "------------------------------" + Fore.RESET)



def winning_conditions():
    win_conditions = []


    for row in range(6):
        for col in range(4):
            
            win_conditions.append([(row, col), (row, col +1), (row, col +2), (row, col +3)])
    

    for row in range(3):
        for col in range(7):
            win_conditions.append([(row, col), (row +1, col), (row +2, col), (row +3, col)])
    

    for row in range(3):
        for col in range(4):
            win_conditions.append([(row, col), (row + 1, col +1), (row +2, col +2), (row +3, col +3)])
    

    for row in range(3):
        for col in range(3, 7):
            win_conditions.append([(row, col), (row + 1, col -1), (row +2, col -2), (row + 3, col -3)])

    return win_conditions

WIN_CONDITIONS = winning_conditions()        
            
def check_win(board, win_conditions, player):
    for condition in win_conditions:
        if all(board[col][row] == player for row, col in condition):
            return True  
    return False  

def player_move(board, player):
    while True:
        try:
            print()
            sleep(0.3)
            col = int(input(random.choice(random_colour) + Style.BRIGHT + "Choose a Column (1-7): " + Style.RESET_ALL).strip()) - 1
            if col < 0 or col > 6:
                raise ValueError(Fore.LIGHTRED_EX + "Invalid Choice!, Please choose between 1 and 7, only")

            if board[col][0] != ' ':
                raise ValueError(Fore.LIGHTRED_EX + "Column is full, Please choose another column")
            
            for row in reversed(range(6)):
                if board[col][row] == ' ':
                    board[col][row] = player
                    return
                
        except ValueError as error:
            print (error)
            
def computer_minimax_move(board, player, computer):
    best_col = FindBestMove(board, player, computer, MAX_DEPTH)  
    for row in reversed(range(6)):
        if board[best_col][row] == ' ':
            board[best_col][row] = computer
            print(Fore.LIGHTGREEN_EX + f"Computer placed disc in column {best_col + 1}")
            sleep(0.7)
            break      
                         
            
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
                    break
                
                elif disc_colour == 2:
                    player1 = YELLOW_DISC
                    player2 = RED_DISC
                    sleep(0.5)
                    break
                
                else:
                    raise ValueError(Fore.LIGHTRED_EX + "Invalid Choice, Please Choose 1 or 2 Only")
            except ValueError as error:
                print(error)
        return player1, player2
                
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
                    break
                
                elif disc_colour == 2:
                    player = YELLOW_DISC
                    computer = RED_DISC
                    break
                
                else:
                    raise ValueError(Fore.LIGHTRED_EX + "Invalid Choice, Please Choose 1 or 2 Only")
            except ValueError as error:
                print(error)
        return player, computer


def game_loop(board, win_conditions, mode):
    if mode == "multi":
        player1, player2 = disc_colour(mode)
        current_player = player1
    elif mode == "single":
        player, computer = disc_colour(mode)
        current_player = player

    moves_counter = defaultdict(int)  
    turn_counter = defaultdict(int)   
    
    while moves_counter['total'] < 42:
        display_board(board)
        
        turn_counter['turn'] += 1
        print(random.choice(random_colour) + Style.BRIGHT + f"Turn {turn_counter['turn']}")
        print()

        if mode == "multi":
            current_player = handle_multi_player_turn(board, current_player, player1, player2)
        elif mode == "single":
            current_player = handle_single_player_turn(board, current_player, player, computer)
                
        moves_counter['total'] += 1
                
        if check_win(board, win_conditions, current_player):
            handle_win(board, mode, current_player, player1, player2, player, computer)
            break
            
        current_player = switch_player(mode, current_player, player1, player2, player, computer)
                
    if moves_counter['total'] == 42 and not check_win(board, win_conditions, current_player):
        handle_draw(board, mode)
        

def handle_multi_player_turn(board, current_player, player1, player2):
    if current_player == player1:
        sleep(0.3)
        print(Fore.RED + "(🔴) It's Player 1's turn!" if player1 == RED_DISC else Fore.YELLOW + "(🟡) It's Player 1's turn!")
        sleep(0.5)
        player_move(board, player1)
    elif current_player == player2:
        sleep(0.3)
        print(Fore.RED + "(🔴) It's Player 2's turn!" if player2 == RED_DISC else Fore.YELLOW + "(🟡) It's Player 2's turn!") 
        sleep(0.5)
        player_move(board, player2)
    return current_player


def handle_single_player_turn(board, current_player, player, computer):
    if current_player == player:
        sleep(0.3)
        print(Fore.RED + "(🔴) It's Your turn!" if player == RED_DISC else Fore.YELLOW + "(🟡) It's Your turn!")
        sleep(0.5)
        player_move(board, player)
    elif current_player == computer:
        sleep(0.3)
        print("Computer's turn...")
        sleep(0.6)
        computer_minimax_move(board, player, computer)
    return current_player


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


def switch_player(mode, current_player, player1, player2, player, computer):
    if mode == "multi":
        if current_player == player1:
            return player2
        elif current_player == player2:
            return player1
    elif mode == "single":
        if current_player == player:
            return computer
        elif current_player == computer:
            return player


def handle_draw(board, mode):
    display_board(board)
    print(Fore.LIGHTCYAN_EX + "It's a Draw!")
    if mode == "multi":
        result_counter_multi['player1']['draws'] += 1
        result_counter_multi['player2']['draws'] += 1
    elif mode == "single":
        result_counter_single['single']['draws'] += 1
            

def handle_play_again(mode, result_counter_single, result_counter_multi):    
    while True:
        try:
            play_again = input("Do you want to play again? (yes/no): ").strip().lower()
            if play_again == "yes" or play_again == "y":
                main()
            elif play_again == "no" or play_again == "n":
                print("\n" + Style.BRIGHT +Fore.LIGHTRED_EX + "Game " + Fore.LIGHTYELLOW_EX + "Results:\n")
                
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
            
    welcome_screen()      
    board = initialise_board()
    display_board(board)
    
    mode = game_mode()
    

    if mode == "single":
        played_single = True      
    elif mode == "multi":
        played_multi = True

        
    win_conditions = winning_conditions()
    game_loop(board, win_conditions, mode)
    
    handle_play_again(mode, result_counter_single, result_counter_multi)
 
 

if __name__ == "__main__":
    main()


 

    

    












 

    

    













    

    











