'''
    Defines Player class, and subclasses Human and Minimax Player.
'''

from othello_board import OthelloBoard


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
       
        
    def get_move(self, board):
        """
        Minimax search implementation
        Based off pseudocode in Chapter 5 of AI: A Modern Approach
        """
        if self.maximizing:
            value, move = self.maxValue(board, self.depth)
        else:
            value, move = self.minValue(board, self.depth)
        return move



    def maxValue(self, board:OthelloBoard, depth:int):
        """
        Returns the best action for the maximizing player
        Based off pseudocode in Chapter 5 of AI: A Modern Approach
        """
        move = (None,None)
        maximizerSymbol = 'X'
        if depth <= 0 or not board.has_legal_moves_remaining(maximizerSymbol):
            return board.count_score(maximizerSymbol), move
        value = float('-inf')
        for c, r in board.generate_legal_moves(maximizerSymbol):
            tempBoard = board.clone_of_board()
            tempBoard.play_move(c, r, maximizerSymbol)
            tempValue, tempMove = self.minValue(tempBoard, depth - 1)
            if tempValue > value:
                value = tempValue
                move = (c, r)
        return value, move

    def minValue(self, board:OthelloBoard, depth:int):
        """
        Returns the best action for the minimizing player
        Based off pseudocode in Chapter 5 of AI: A Modern Approach
        """
        move = (None,None)
        minimizerSymbol = 'O'
        if depth <= 0 or not board.has_legal_moves_remaining(minimizerSymbol):
            return board.count_score(minimizerSymbol), move
        value = float('inf')
        for c, r in board.generate_legal_moves(minimizerSymbol):
            tempBoard = board.clone_of_board()
            tempBoard.play_move(c, r, minimizerSymbol)
            tempValue, tempMove = self.maxValue(tempBoard, depth - 1)
            if tempValue < value:
                value = tempValue
                move = (c, r)
        return value, move
