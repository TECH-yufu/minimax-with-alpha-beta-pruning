# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 14:51:35 2021

"""

import numpy as np
import cv2
import pyautogui
import win32api, win32con
import time
import keyboard

from policy import *
from env import *


def trim_image1(image, pos):
    assert type(pos) == str
    
    img_h = image.shape[0]
    
    if pos == 'top':
        cap = 0
        for i in range(img_h):
            if np.all([x == 0 for x in image[i]]):
                cap = i
                break
            else:
                pass
                
        return image[cap:, :], cap
                
    elif pos == 'bottom':
        cap = img_h
        for i in range(img_h-1,-1,-1):
            if np.all([x == 0 for x in image[i]]):
                cap = i
                break
            else:
                pass
            
        return image[:cap+1, :], img_h - cap-1

def trim_image2(image, pos):
    assert type(pos) == str
    
    img_h = image.shape[0]
    
    if pos == 'top':
        cap = 0
        for i in range(img_h):
            if np.all([x == 0 for x in image[i]]):
                pass
            else:
                cap = i 
                break
                
        return image[cap:, :], cap
                
    elif pos == 'bottom':
        cap = img_h
        for i in range(img_h-1,-1,-1):
            if np.all([x == 0 for x in image[i]]):
                pass
            else:
                cap = i
                break
            
        return image[:cap+1, :], img_h - cap-1

def trimmed_image(threshold_image):
    # remove all the other things on the page by trimming
    img, a = trim_image1(threshold_image, 'top')
    img, b = trim_image1(img, 'bottom')
    img, c = trim_image2(img, 'top')
    img, d = trim_image2(img, 'bottom')
    img, e = trim_image1(img, 'top')
    img, f = trim_image1(img, 'bottom')
    img, g = trim_image2(img, 'bottom')
    img, h = trim_image1(img, 'bottom')
 
    # make into 1080 x 1920 image again
    img = np.vstack((np.zeros((a+c+e,1920)), img, np.zeros((b+d+f+g+h,1920)))).astype("uint8")
    
    return img

def getScreenshot():
    # get screenshot of tictactoe game
    img = pyautogui.screenshot()
    img = np.array(img)
    
    return img


def boardState():
    """
    

    Returns
    -------
    board : tictactoe board
    coordinates : coordinates of each tile on the board

    """
    # time.sleep(2)
    board = np.array([[0,0,0],[0,0,0],[0,0,0]])
    coordinates = np.array([[None,None,None],[None,None,None],[None,None,None]])
    
    img = getScreenshot()
    
    # turn into grayscale
    img_g =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_h, img_w = img_g.shape
    
    # use Otsu threshold
    ret,thresh = cv2.threshold(img_g, 0,255,cv2.THRESH_OTSU)
    
    # trim thresolded image
    thresh = trimmed_image(thresh)
    
    #find and draw ALL contours.
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img, contours, -1, (0,255,0), 5)
    
    # DISPLAY PURPOSES
    # winname = "Test"
    # cv2.namedWindow(winname)        # Create a named window
    # cv2.moveWindow(winname, 40,30)  # Move it to (40,30)
    # cv2.imshow(winname, thresh)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # get last contour (whole board)
    cnt = contours[-1]
    x,y,w,h = cv2.boundingRect(cnt)
    
    coordinate_x = [x, x+w]
    coordinate_y = [y, y+h]
    
    p,q = max(coordinate_x) - min(coordinate_x), max(coordinate_y) - min(coordinate_y)
    # print(p,q)
    
    # get rough coordinates
    for i in range(3):
        for j in range(3):
            coordinates[j][i] = (int(x+(i+1)*np.round(p/3)), int(y+(j+1)*np.round(q/3)))
            
    # loop through all contours
    for contour in contours: 
        area = cv2.contourArea(contour)
        if area < 25000:
            x,y,w,h = cv2.boundingRect(contour)
            
            hull = cv2.convexHull(contour)
            hull_area = cv2.contourArea(hull)
            solidity = area / hull_area
            
            # Get board state and coordinates of each tile.
            if (area > 10000 and solidity > 0.5) or (area < 10000 and solidity < 0.5):
                coordX = int(np.round(3*(x-min(coordinate_x)) / (max(coordinate_x) - min(coordinate_x))))
                coordY = int(np.round(3*(y-min(coordinate_y)) / (max(coordinate_y) - min(coordinate_y))))
                # print(area, solidity)
                # print((x,y,w,h))
                # print(coordX)
                # print(coordY)
                
                coordinates[coordY][coordX] = (x,y)
        
                
                if solidity > 0.5:
                    # insert O
                    board[coordY][coordX] = 2
                else:
                    # insert X
                    board[coordY][coordX] = 1
                
                # FOR DISPLAY PURPOSES
                # winname = "Test"
                # cv2.namedWindow(winname)        # Create a named window
                # cv2.moveWindow(winname, 40,30)  # Move it to (40,30)
                # cv2.imshow(winname, thresh[y:y+h,x:x+w])
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                
    return board.reshape(1,-1)[0], coordinates.reshape(1,-1)[0]


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
    
    
def performAction(coordinates, action):
    if action is not None:
        click(coordinates[action])
    
def agent(policy):
    score = {"PLAYER": 0, "TIE": 0, "COMPUTER": 0}
    
    while True:
        # press 'q' to start and get initial board state
        if keyboard.is_pressed('q'):
            time.sleep(2)
            board, coordinates = boardState()
            print(board.reshape(3,3))
        
            while True:
                # press 'w' to make a move
                if keyboard.is_pressed('w'):
                    
                    if policy == "minimax":
                        d = getDepth(board)
                        alpha = -np.inf
                        beta = np.inf
                        _,action = minimax(board, d, alpha, beta, True)
                    
                    else:
                        action = randomPolicy(board)
                    
                    if getWinner(board) is not None:
                        score = updateScore(board, score)
                        print(
"""
The score is:
Player: {}
Tie: {}
Computer: {}
""".format(score["PLAYER"], score["TIE"], score["COMPUTER"]))
    
                        click(coordinates[0])
                        break    
                    
                    performAction(coordinates, action)
                    
                    

                    time.sleep(2)
                    board, coordinates = boardState()
                    print(board.reshape(3,3))
    
                    if getWinner(board) is not None:
                        score = updateScore(board, score)
                        print(
"""
The score is:
Player: {}
Tie: {}
Computer: {}
""".format(score["PLAYER"], score["TIE"], score["COMPUTER"]))
    
                        click(coordinates[0])
                        break