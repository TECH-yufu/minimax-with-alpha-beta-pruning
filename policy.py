# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 15:50:27 2021

"""

import numpy as np
from random import choice


def actionSpace():
    """
    Possible actions in tic-tac-toe

    """
    return set(np.arange(9))

def possibleActions(board):
    """
    Get set of possible actions to perform

    """
    moves = np.where(board != 0)[0]
    possibleActions = list(actionSpace() - set(moves))
    
    return possibleActions

def getDepth(board):
    """
    Get depth of the board

    """
    
    
    availActions = possibleActions(board)
    return len(availActions)

def getWinner(board):
    """
    Determine a winner from the board

    """
    
    board = board.reshape(3,3)
    
    for row in range(3):
        if board[row,0] == board[row,1] and board[row,1] == board[row,2] and board[row,0] != 0:
            if board[row,0] == 1:
                return "PLAYER"
            elif board[row,0] == 2:
                return "COMPUTER"
    
    for col in range(3):
        if board[0,col] == board[1,col] and board[1,col] == board[2,col] and board[0,col] != 0:
            if board[0, col] == 1:
                return "PLAYER"
            elif board[0, col] == 2:
                return "COMPUTER"

    if board[0,0] == board[1,1] and board[1,1] == board[2,2] and board[0,0] != 0:
        if board[0,0] == 1:
            return "PLAYER"
        elif board[0,0] == 2:
            return "COMPUTER"
    if board[0,2] == board[1,1] and board[1,1] == board[2,0] and board[0,2] != 0:
        if board[0,2] == 1:
            return "PLAYER"
        elif board[0,2] == 2:
            return "COMPUTER"
        
    board = board.reshape(9)
    if len(possibleActions(board)) == 0:
        return "TIE"

    return None

###  POLICIES
def randomPolicy(board):
    """
    Perform a random action based on board.

    """
    availActions = possibleActions(board)
    action = choice(availActions)

    return action

def minimax(board, depth, alpha, beta, maximisingPlayer):
    """
    Minimax algorithm with alpha-beta pruning

    """
    
    # utility score
    utility = {"PLAYER": 10,
              "COMPUTER": -10,
              "TIE": 0}
    
    
    if getWinner(board) is not None:
        if getWinner(board) == "PLAYER":
            result = utility["PLAYER"] * (depth+1)
        elif getWinner(board) == "COMPUTER":
            result = utility["COMPUTER"] * (depth+1)
        else:
            result = utility["TIE"]
        
        return result, None

    V = {}
    if maximisingPlayer:
        availActions = possibleActions(board)
        
        for u in availActions:
            zeros = np.zeros(9)
            zeros[u] = 1
        
            new_board = board + zeros
            
            V[u], _ = minimax(new_board, depth-1, alpha, beta, False)
            alpha = max(alpha, V[u])
            if beta <= alpha:
                break
            
        best_action = max(V, key=V.get)
            
    else: 
        availActions = possibleActions(board)

        for u in availActions:
            zeros = np.zeros(9)
            zeros[u] = 2
            new_board = board + zeros
            
            V[u], _ = minimax(new_board, depth-1, alpha, beta, True)
            beta = min(beta, V[u])
            if beta <= alpha:
                break
        best_action = min(V, key=V.get)
            


    return V[best_action], best_action

