# Introduction
This project implements minimax for the board game Go. The minimax implementation utilizes both alpha-beta pruning to only consider promising moves, as well as a time-based cutoff to prevent moves from taking over 10 seconds.

## Results
The minimax implementation was tested against a player for a 4x4 and 8x8 board. The player went first in both cases. The results are as follows:

### Results for 4x4 Board Games

| Depth | Winner of Game | Changes in Minimax Moves | Average Seconds per Move |
|-------|----------------|--------------------------|--------------------------|
| 5     | Minimax        | No                       |      0.0210              |
| 3     | Minimax        | No                       |      0.0092              |
| 2     | Minimax        | Yes                      |      0.0047              |
| 1     | Minimax        | Yes                      |      0.0024              |

### Results for 8x8 Board Games
| Depth | Winner of Game | Changes in Minimax Moves | Average Seconds per Move |
|-------|----------------|--------------------------|--------------------------|
| 5     | Minimax        | No                       | 1.4896                   |
| 2     | Minimax        | Unknown                  | 0.0408                   |

## Discussion
The minimax agent outperformed the human player in each of the tests. The average time per move for the minimax agent increases both with larger boards and depths. The larger board size increases the amount of moves the minimax agent needs to consider at each depth, while the depth increases the height of the search tree. The board size had more noticeable effects on move times than depth. The time complexity of making a move is O(b^d) without pruning and O(b^(d/2)) with alpha-beta pruning. There were noticeable changes in the minimax agent's moves in the 4x4 games when the depth was reduced to 2, however these changes could not be observed in the 8x8 games. 


## How to play a game:

1. Run `python3 game_driver.py [player_type] [player_type] [optional: board size] [optional: depth]`.
2. Choose `human`, or `minimax` as the player types.
3. Follow the prompts to choose where to place stones.


## References
Originally created by Erich Kramer at OSU for Professor Rebecca Hutchinson.
Cleaned up by Rob Churchill.
Implemented by Matthew O'Malley-Nichols
