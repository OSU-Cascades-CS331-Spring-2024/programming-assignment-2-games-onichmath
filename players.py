'''
    Defines Player class, and subclasses Human and Minimax Player.
'''

from othello_board import OthelloBoard
from time import time


class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()


class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol)

    def clone(self):
        return HumanPlayer(self.symbol)
        
#PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return col, row


class MinimaxPlayer(Player):

    def __init__(self, symbol, depth=5, maximizing=True):
        Player.__init__(self, symbol)
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'
        self.depth = depth
        self.maximizing = maximizing
        self.timer = 0
        self.moves = 0

    def __del__(self):
        print(f"Player {self.symbol} made {self.moves} moves in an average {(self.timer / self.moves) :.4f} seconds.")
       
        
    def get_move(self, board):
        """
        Minimax search implementation
        Based off pseudocode in Chapter 5 of AI: A Modern Approach
        """
        self.moves += 1
        start = time()
        alpha = float('-inf')
        beta = float('inf')
        move_start_time = time()
        if self.maximizing:
            value, move = self.maxValue(board, self.depth, alpha, beta, move_start_time)
        else:
            value, move = self.minValue(board, self.depth, alpha, beta, move_start_time)
        end = time()
        self.timer += end - start
        return move

    def maxValue(self, board:OthelloBoard, depth:int, alpha, beta, start_time):
        """
        Returns the best action for the maximizing player
        Based off pseudocode in Chapter 5.2.3 of AI: A Modern Approach
        """
        move = (None,None)
        maximizerSymbol = 'X'
        if depth <= 0 or board.isCutoff(maximizerSymbol, start_time):
            return board.heuristic(), move
        value = float('-inf')
        for c, r in board.generate_legal_moves(maximizerSymbol):
            tempBoard = board.clone_of_board()
            tempBoard.play_move(c, r, maximizerSymbol)
            tempValue, tempMove = self.minValue(tempBoard, depth - 1, alpha, beta, start_time)
            if tempValue > value:
                value = tempValue
                move = (c, r)
                alpha = max(alpha, value)
            if value >= beta:
                return value, move
        return value, move

    def minValue(self, board:OthelloBoard, depth:int, alpha, beta, start_time):
        """
        Returns the best action for the minimizing player
        Based off pseudocode in Chapter 5.2.3 of AI: A Modern Approach
        """
        move = (None,None)
        minimizerSymbol = 'O'
        if depth <= 0 or board.isCutoff(minimizerSymbol, start_time):
            return board.heuristic(), move
        value = float('inf')
        for c, r in board.generate_legal_moves(minimizerSymbol):
            tempBoard = board.clone_of_board()
            tempBoard.play_move(c, r, minimizerSymbol)
            tempValue, tempMove = self.maxValue(tempBoard, depth - 1, alpha, beta, start_time)
            if tempValue < value:
                value = tempValue
                move = (c, r)
                beta = min(beta, value)
            if value <= alpha:
                return value, move
        return value, move
