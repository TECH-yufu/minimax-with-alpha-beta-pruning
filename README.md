# Tic-tac-toe: Minimax algorithm with alpha-beta pruning

Tic-tac-toe is a considered a solved game due to its shallow depth compared to other board games, e.g. chess. With "only" 255168 [[1]](#1) possible games of tic-tac-toe it is therefore feasible to search for the optimal move for any given board position using the minimax algorithm. With the minimax algorithm, the agent chooses an optimal action under the assumption that the opponent plays optimally. Alpha-beta pruning is used to remove redundant actions which are known to be suboptimal and speeds up the search.

The agent plays against the computer at https://playtictactoe.org/. OpenCV is used to interpret the environment, and the agent interacts with the environment using simulated mouse clicks.

# How to use
1. Clone repository
2. `cd` to the cloned folder
3. Go to https://playtictactoe.org/
4. Open and run `main.py`. Press 'w' to make an action.

![undefeated](https://media.discordapp.net/attachments/344157424615161856/868945568662183986/unknown.png?width=569&height=612)

## References
<a id="1">[1]</a> 
http://www.se16.info/hgb/tictactoe.htm
