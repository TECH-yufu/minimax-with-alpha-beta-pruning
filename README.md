# minimax-with-alpha-beta-pruning
The tic-tac-toe agent plays against the computer at https://playtictactoe.org/

Tic-tac-toe is a considered a solved game due to its shallow depth compared to other board games, e.g. chess. This means that all end-game states can be computed from any given board state.

Currently, the agent relies on pixel values and (x,y) coordinates to interact with the board. This is bad for a number of reasons:
- Non-compatible with different screen sizes/resolutions 
- Using pixel values to determine the board state is a quick implementation but scales poorly.
These shortcomings could potentially be fixed with OpenCV/PyAutoGUI

![undefeated](https://media.discordapp.net/attachments/344157424615161856/868945568662183986/unknown.png?width=569&height=612)
