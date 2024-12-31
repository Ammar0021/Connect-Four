from utility import check_win, WIN_CONDITIONS
import time
import hashlib

MAX_DEPTH = 5 # You can adjust this based on your needs

# Transposition table to store already evaluated board positions
transposition_table = {}

def board_hash(board):
    '''Creates a unique hashable representation of the board'''
    board_string = ''.join([''.join(col) for col in board])
    return hashlib.sha1(board_string.encode()).hexdigest()

def HeuristicEvaluations(board, player, computer, WIN_CONDITIONS):
    score = 0
    centre_col = 3
    
    '''Centre Priority'''
    centre_count = sum(1 for row in range(6) if board[centre_col][row] == computer)
    score += centre_count * 3
    
    for condition in WIN_CONDITIONS:
        player_count = sum(1 for row, col in condition if board[col][row] == player)
        computer_count = sum(1 for row, col in condition if board[col][row] == computer)
        
        if player_count > 0 and computer_count == 0:
            score -= 10 ** player_count  # Penalty for computer, encourages blocking winning moves from the human player
        elif computer_count > 0 and player_count == 0:
            score += 10 ** computer_count  # Reward for computer, encourages winning moves for the computer, exponents used to HIGHLY Penalise or Reward
    return score

def MinimaxAlphaBeta(board, depth, alpha, beta, MaximisingPlayer, player, computer, WIN_CONDITIONS):
    board_key = board_hash(board)
    
    if board_key in transposition_table:
        return transposition_table[board_key]

    if (depth == 0 or 
        check_win(board, WIN_CONDITIONS, computer) or 
        check_win(board, WIN_CONDITIONS, player) or 
        all(board[col][0] != ' ' for col in range(7))):
        score = HeuristicEvaluations(board, player, computer, WIN_CONDITIONS)
        transposition_table[board_key] = score
        return score

    if MaximisingPlayer:
        MaxEval = float('-inf')
        for col in range(7):
            if board[col][0] == ' ':
                for row in reversed(range(6)):
                    if board[col][row] == ' ': # Finds empty cell
                        board[col][row] = computer # Places disc in empty cell
                        
                        eval = MinimaxAlphaBeta(board, depth-1, alpha, beta, False, player, computer, WIN_CONDITIONS) # Recursion
                        '''
                        - depth-1 makes algorithm reduce the depth each recursive call, allows to explore deeper
                        - alpha is best value that maximiser (computer) can currently guarantee
                        - beta is current best value that minimiser can guarantee
                        - False means its the minimsing player's turn (it flips each recursive call)
                        '''
                        
                        board[col][row] = ' '
                        MaxEval = max(MaxEval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:  # This Triggers Pruning
                            break
        transposition_table[board_key] = MaxEval
        return MaxEval
    
    else:
        MinEval = float('inf')
        for col in range(7):
            if board[col][0] == ' ':
                for row in reversed(range(6)):
                    if board[col][row] == ' ':
                        board[col][row] = player
                        
                        eval = MinimaxAlphaBeta(board, depth-1, alpha, beta, True, player, computer, WIN_CONDITIONS)
                        board[col][row] = ' '
                        MinEval = min(MinEval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
        transposition_table[board_key] = MinEval
        return MinEval

def quiescence_search(board, alpha, beta, player, computer, WIN_CONDITIONS):
    '''Extends the search in unstable positions to avoid misleading evaluations.
    Evaluates until positions become stable (quiet)'''
    stand_pat = HeuristicEvaluations(board, player, computer, WIN_CONDITIONS)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    # Generate and evaluate capture moves (if any)
    for col in range(7):
        if board[col][0] == ' ':
            for row in reversed(range(6)):
                if board[col][row] == ' ':
                    board[col][row] = computer
                    score = -quiescence_search(board, -beta, -alpha, player, computer, WIN_CONDITIONS)
                    board[col][row] = ' '
                    if score >= beta:
                        return beta
                    if score > alpha:
                        alpha = score
    return alpha

def iterative_deepening(board, depth, player, computer, WIN_CONDITIONS):
    '''Repeatedly searches deeper levels one-by-one, allowing quick move decisions.
    Also stops searching if it takes too long'''
    start_time = time.time()
    best_col = None
    best_score = float('-inf')

    for d in range(1, depth + 1):
        col, score = deepening_search(board, d, player, computer, WIN_CONDITIONS)
        if score > best_score:
            best_score = score
            best_col = col
        if time.time() - start_time > 2:  # Set a time limit for the search
            break
    return best_col

def deepening_search(board, depth, player, computer, WIN_CONDITIONS):
    '''Searches the board to a specific depth to evaluate the best move'''
    best_score = float('-inf')
    best_col = None

    for col in range(7):
        if board[col][0] == ' ':
            for row in reversed(range(6)):
                if board[col][row] == ' ':
                    board[col][row] = computer
                    score = MinimaxAlphaBeta(board, depth, float('-inf'), float('inf'), False, player, computer, WIN_CONDITIONS)
                    board[col][row] = ' '
                    if score > best_score:
                        best_score = score
                        best_col = col
    return best_col, best_score

def FindBestMove(board, player, computer):
    depth = MAX_DEPTH
    return iterative_deepening(board, depth, player, computer, WIN_CONDITIONS)
