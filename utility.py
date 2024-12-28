'''I created this due to a circular import error,
these functions are SHARED in both main.py and MinimaxAlphaBeta.py'''

def winning_conditions():
    win_conditions = []

    for row in range(6):
        for col in range(4):
            win_conditions.append([(row, col), (row, col + 1), (row, col + 2), (row, col + 3)])

    for row in range(3):
        for col in range(7):
            win_conditions.append([(row, col), (row + 1, col), (row + 2, col), (row + 3, col)])

    for row in range(3):
        for col in range(4):
            win_conditions.append([(row, col), (row + 1, col + 1), (row + 2, col + 2), (row + 3, col + 3)])

    for row in range(3):
        for col in range(3, 7):
            win_conditions.append([(row, col), (row + 1, col - 1), (row + 2, col - 2), (row + 3, col - 3)])

    return win_conditions

WIN_CONDITIONS = winning_conditions()

def check_win(board, win_conditions, player):
    for condition in win_conditions:
        if all(board[col][row] == player for row, col in condition):
            return True
    return False