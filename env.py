# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 22:03:20 2021


"""
import numpy as np
from policy import *

def updateScore(board, score):
    """
    Update score after a game


    """
    winner = getWinner(board)
    
    if winner == "PLAYER":
        score["PLAYER"] += 1
    elif winner == "COMPUTER":
        score["COMPUTER"] += 1
    elif winner == "TIE":
        score["TIE"] += 1
    
    return score

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
