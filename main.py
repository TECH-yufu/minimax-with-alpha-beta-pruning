# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 00:40:47 2021


"""

import numpy as np
import keyboard
import time
from agent import * 
from policy import *
from env import *


if __name__ == "__main__":       
    agent(policy='minimax')