# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 11:28:47 2021

"""

import time
from PIL import ImageGrab, ImageOps, Image
import numpy as np
import keyboard
import win32api, win32con
from random import choice


def pixelValue(coordinate):
    """
    Get pixel value of the desired area

    Parameters
    ----------
    coordinate : tuple

    Returns
    -------
    val : int
        sum of pixel value * quantity 
        of the desired area

    """
    x,y = coordinate
    image = ImageGrab.grab(bbox=(x,y,x+150,y+150))
    grayImage = ImageOps.grayscale(image)
    val = sum([i*j for i,j in grayImage.getcolors()])
        
    return val

def boardState(pixelValues):
    """
    Get current board state
    1 = X
    2 = O

    Parameters
    ----------
    pixelValues : array

    """
    
    board_state = np.zeros(9)

    for val,i in zip(pixelValues,range(len(pixelValues))):
        if val in [1520771,763248]:
            board_state[i] = int(1)
        elif val > 1520771 or val in [884732, 899906, 910740]:
            board_state[i] = int(2)
            
    return tuple(board_state.astype(int))

def click(coordinate):
    """
    Click the board

    Parameters
    ----------
    coordinate : tuple

    Returns
    -------
    None.

    """
    x,y = coordinate
    win32api.SetCursorPos((x-20,y-20))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    
def actionSpace():
    """
    Possible actions in tic-tac-toe

    """
    return set(np.arange(9))

def possibleActions(board):
    """
    Get set of possible actions to perform

    """
    moves = np.where(np.array(board) != 0)[0]
    possibleActions = list(actionSpace() - set(moves))
    
    return possibleActions


def isTerminalState(s):
    """
    Test if board is in a terminal state

    """
    terminate = np.array([763248, 884732, 899906, 910740])
    isTerminal = np.any([s[i] in terminate for i in range(len(s))])
    
    return isTerminal

def getWinner(board):
    """
    Determine a winner from the board

    """
    
    board = np.array(list(board)).reshape(3,3)
    
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
        
def updateScore(s, score):
    """
    Update score after a game


    """
    player_wins = 1520771
    
    if np.any([s[i] == player_wins for i in range(len(s))]):
        score["PLAYER"] += 1
    elif np.any([s[i] > player_wins for i in range(len(s))]):
        score["COMPUTER"] += 1
    else:
        score["TIE"] += 1
    
    return score
    
def getDepth(board):
    """
    Get depth of the board

    """
    
    
    availActions = possibleActions(board)
    return len(availActions)


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
            new_board = np.array(list(board)) + zeros
            
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
            new_board = np.array(list(board)) + zeros
            
            V[u], _ = minimax(new_board, depth-1, alpha, beta, True)
            beta = min(beta, V[u])
            if beta <= alpha:
                break
        best_action = min(V, key=V.get)
            


    return V[best_action], best_action

# where to click to make an action on the 3x3 board
coordinates = [(682,209), (882,209), (1082,209),
                (682,409), (882,409), (1082,409),
                (682,609), (882,609), (1082,609)]





def agent(policy):
    score = {"PLAYER": 0, "TIE": 0, "COMPUTER": 0}
    
    while True:
        # press 'q' to start and get initial board state
        if keyboard.is_pressed('q'):
            time.sleep(2)
            boards = []
            s = [pixelValue(i) for i in coordinates]
            board = boardState(s)
            print(s)
            print(np.array(list(board)).reshape(3,3))
    
            boards.append(board)
    
            while True:
                # press 'w' to make a move
                if keyboard.is_pressed('w'):
                    
                    
                    if policy == "ai":
                        d = getDepth(board)
                        alpha = -np.inf
                        beta = np.inf
                        _,action = minimax(board, d, alpha, beta, True)
                    
                    else:
                        action = randomPolicy(board)
    
                    click(coordinates[action])
    
                    time.sleep(1)
                    if len(boards) > 0 and board not in boards:
                        boards.append(board)
    
                    s = [pixelValue(i) for i in coordinates]
                    board = boardState(s)
                    print(s)
                    print(np.array(list(board)).reshape(3,3))
    
                    if len(boards) > 0 and board not in boards:
                        boards.append(board)
    
                    if isTerminalState(s):
                        score = updateScore(s, score)
                        print(
"""
The score is:
Player: {}
Tie: {}
Computer: {}
""".format(score["PLAYER"], score["TIE"], score["COMPUTER"]))
    
                        click((879,403))
                        break
                    
if __name__ == "__main__":       
    agent(policy='ai')

# coordinates = [(682,209), (882,209), (1082,209),
#                (682,409), (882,409), (1082,409),
#                (682,609), (882,609), (1082,609)]
# time.sleep(2)

# s = [pixelValue(i) for i in coordinates]
# board = boardState(s)

# terminate = np.array([763248, 884732, 899906, 910740])

# d = getDepth(board)
# # _, best_action = minimax(board, getDepth(board), True)
# _, best_action = minimax(board, getDepth(board), -np.inf, np.inf, True)
# print(best_action)






