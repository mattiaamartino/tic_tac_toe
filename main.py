import random
from math import inf
from copy import copy
import os

'''
Algorithm that implements both a random computer and a AI playing tic-tac-toe
against the user. The AI is a Minimax, that in this specific game wins all the
time if it starts, and in the worst case (a rational user that begins) draws.
'''



# We define the initial board as all empty cells
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

# We give the user a value -1 and the computer (or better the algorithm) 1, for
# game-theoretical coherence

user = -1
comp = 1

def check_win(board, player):   
    '''
    Takes as input is the current board and the player.
    The function checks at the end of each turn if the player has won the game.
    The player wins he has 3 on a row, column or diagonal of its symbol
    (X or O).
    If one of the players won it prints a string and ends the game.
    '''
    
    row_state = [[board[0][0], board[0][1], board[0][2]],
                 [board[1][0], board[1][1], board[1][2]],
                 [board[2][0], board[2][1], board[2][2]]]
    column_state = [[board[0][0], board[1][0], board[2][0]],
                    [board[0][1], board[1][1], board[2][1]],
                    [board[0][2], board[1][2], board[2][2]]]
    diag_state = [[board[0][0], board[1][1], board[2][2]],
                  [board[0][2], board[1][1], board[2][0]]]
    
    if player == 'gen':
        return check_win(board, user) or check_win(board, comp)
    
    
    if [player, player, player] in [row_state, column_state, diag_state]:
        print(f"{player} won!")
        return True
    
    
def freesquares(board):
    free = list()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if not board[i][j]:
                free.append([i, j])
    return free

    
def score_val(board):
    '''
    Support function for minimax. Takes the board as input and returns a different
    score if for the win of the user or of the computer or a draw. Also in this
    case the values are due to game theory.
    ''' 
    if check_win(board, user):
        return -1
    elif check_win(board, comp):
        return 1
    else:
        return 0
    

def move(hor, vert, player):
    '''
    Takes as input horizontal and vertical coordinates of the selected square, 
    together with the player. If the move is valid change the state of the square
    '''
    
    if not board[hor][vert]:
        board[hor][vert] = player
        return True
    return False
    
def minimax(board, depth, player):
    
    if player == comp:
        best_move = [-1, -1]
        best_score = -inf
        
    if player == user:
        best_move = [-1,-1]
        best_score = inf
    
    # Checks if the game is over. It is the case if no more cells are empty
    # (depth = 0) or the check_win function returns True
    if depth == 0 or check_win(board, player):
        return best_move, score_val(board)
    
    free = freesquares(board)
    
    for square in free:
        
        hor, ver = square[0], square[1]
        board[hor][ver] = player
        move, score = minimax(board, depth-1, -player)  # We take our new board, we diminish by one the free squares and change player
        board[hor][ver] =  0    #We got our score and we reset the free square
        move[0], move[1] = hor, ver
        
        if player == comp:
            if score > best_score:
                best_move, best_score = move, score
        if player == user:
            if score < best_score:
                best_move, best_score = move, score
        
        
    return best_move, best_score



def table(board, user):
    
    corr = {0: ' ', -1: 'X', 1:'O'}
    
    print('\n'+'---------------')
    
    
    for r in board:
        for square in r:
           sym = corr[square]
           print(f"| {sym} |", end='')
        print("\n"+'---------------')
    

def user_move():
    
    depth = len(freesquares(board))
    if depth == 0 or check_win(board, user):
        return
    
    moves_dict = {1: [0, 0], 2: [0, 1], 3: [0, 2],
                  4: [1, 0], 5: [1, 1], 6: [1, 2],
                  7: [2, 0], 8: [2, 1], 9: [2, 2]}
    
    choice = 0
    table(board, user)
    
    while choice not in moves_dict:
        choice = int(input("Select a number between 1 and 9: "))
        if not isinstance(choice, int):
            raise TypeError('The input must be a number')
        
        pos = moves_dict[choice]
        if not move(pos[0], pos[1], user):
            choice = int(input("That square is already taken. Select another one: "))
            
    move(pos[0], pos[1], user)
            

def comp_move():
    
    depth = len(freesquares(board))
    if depth == 0 or check_win(board, user):
        return
    
    table(board, comp)
    
    if depth == 9:
        hor = random.choice([0, 2])
        ver = random.choice([0, 2])
    else:
        choice = minimax(board, depth, comp)
        hor, ver = choice[0][0], choice[0][1]
    
    move(hor, ver, comp)
    

def main():
    
    start = ''
    
    while start != 'y' and  start != 'n':
        start = input("Do you want to start? (y/n): ").lower()
        
    depth = len(freesquares(board))
    
    
    while depth>0 and not check_win(board, 'gen'):
        if start == 'n':
            comp_move()
            start = ''
        
        user_move()
        comp_move()
        
    if check_win(board, user):
        print("The user wins!")
    elif check_win(board, comp):
        print("The computer wins!")
    else:
        print("Draw!")
        
    exit()
        
        
    
        
    
    
    
    

