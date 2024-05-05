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

    def __init__(self, symbol):
        Player.__init__(self, symbol)
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'
        self.depth = 5
       
        
    def get_move(self, board):
        """
        Minimax search implementation
        """
        # TODO: Find out if max or min player
        value, move = self.maxValue(board, self.depth)
        return 

    def maxValue(self, board:OthelloBoard, depth:int):
        """
        Returns the best action for the maximizing player
        """
        move = (None,None)
        if depth == 0 or not board.has_legal_moves_remaining(self.symbol):
            return board.count_score(self.symbol), move
        value = float('-inf')
        for c, r in board.generate_legal_moves(self.symbol):
            tempValue, tempMove = self.minValue(board, depth - 1)
            if tempValue > value:
                value = tempValue
                move = tempMove
        return value, move

    def minValue(self, board:OthelloBoard, depth:int):
        pass

    def minimax(self, board:OthelloBoard, depth:int, maximizingPlayer:bool):
        """
        Returns the best action for the player
        Written based off AI: A Modern Approach Chapter 5 and https://en.wikipedia.org/wiki/Minimax#Pseudocode
        """
        if depth == 0 or not board.has_legal_moves_remaining(self.symbol):
            # If terminal, return utility
            return board.count_score(self.symbol)
        minimaxValue = 0
        moves = (-1,-1)
        if maximizingPlayer:
            minimaxValue = float('-inf')
            # For move in legal moves:
            # maxValue = max of minValue and minimax(move, depth-1, maximizingPlayer)
            for c, r in board.generate_legal_moves(self.symbol):
                tempMinimaxValue = self.minimax(board, depth - 1, not maximizingPlayer)
                if tempMinimaxValue > minimaxValue:
                    minimaxValue = max(minimaxValue, self.minimax(board, depth - 1, maximizingPlayer))
                    moves = (c, r)
        else:
            minimaxValue = float('inf')
            # For move in legal moves:
            # maxValue = min of maxValue and minimax(move, depth-1, maximizingPlayer)
            for c, r in board.generate_legal_moves(self.symbol):
                tempMinimaxValue = self.minimax(board, depth - 1, not maximizingPlayer)
                if tempMinimaxValue < minimaxValue:
                    minimaxValue = min(minimaxValue, self.minimax(board, depth - 1, maximizingPlayer))
                    moves = (c, r)
        return minimaxValue, moves




