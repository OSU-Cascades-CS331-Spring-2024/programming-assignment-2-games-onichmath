'''
    Defines Othello Board class and supporting functions.
'''

from board import *
from time import time


class OthelloBoard(Board):
    def __init__(self, rows, cols, p1, p2):
        Board.__init__(self, rows, cols)
        self.p1_symbol = p1
        self.p2_symbol = p2


#PYTHON: this function is substitute for clone. call as New = Old.clone_of_board()
    def clone_of_board(self):
        tmp = OthelloBoard(self.cols, self.rows, self.p1_symbol, self.p2_symbol)
        tmp.grid = copy.deepcopy(self.grid)
        return tmp

    def initialize(self):
        self.set_cell(self.cols //2 -1, self.rows //2 -1,   self.p1_symbol)
        self.set_cell(self.cols //2,    self.rows //2,      self.p1_symbol)
        self.set_cell(self.cols //2 -1, self.rows //2,      self.p2_symbol)
        self.set_cell(self.cols //2,    self.rows //2 -1,   self.p2_symbol)

#PYTHON: Instead of having side effects this function now returns a TUPLE
    def set_coords_in_direction(self, col, row, d):  # D=direction
        if d.name == 'N':
            row += 1
        elif d.name == 'NE':
            col+=1
            row+=1
        elif d.name == 'E':
            col+=1
        elif d.name == 'SE':
            col+=1
            row-=1
        elif d.name == 'S':
            row-=1
        elif d.name == 'SW':
            col-=1
            row-=1
        elif d.name == 'W':
            col-=1
        elif d.name == 'NW':
            col-=1
            row+=1
        else:
            print("Invalid Direction.")
        return  col, row

#Recursively travel in a direction
    def check_endpoint(self, col, row, symbol, d, match_symbol):#match is bool type
        if not self.is_in_bounds(col, row) or self.is_cell_empty(col,row):
            return False
        else:
            if match_symbol:
                if self.get_cell(col, row) == symbol:
                    return True
                else:
                    (next_col, next_row) = self.set_coords_in_direction(col, row, d)
                    return self.check_endpoint(next_col, next_row, symbol, d, match_symbol)
            else:
                if self.get_cell(col, row) == symbol:
                    return False
                else:
                    (next_col, next_row) = self.set_coords_in_direction(col, row, d)
                    return self.check_endpoint(next_col, next_row, symbol, d, not match_symbol)

    def is_legal_move(self, col, row, symbol):
        result = False
        if not self.is_in_bounds(col, row) or not self.is_cell_empty(col, row):
            return False
        for d in Direction: #enum from board.py
            (next_col, next_row) = self.set_coords_in_direction(col, row, d)
            if self.check_endpoint(next_col, next_row, symbol, d, False):
                return True
        return False
        
    def flip_pieces_helper(self, col, row, symbol, d):
        if self.get_cell(col, row) == symbol:
            return 0
        else:
            self.set_cell(col,row, symbol)
            (next_col, next_row) = self.set_coords_in_direction(col, row, d)
            return 1+ self.flip_pieces_helper(next_col, next_row, symbol, d)



    def flip_pieces(self, col, row, symbol):
        pieces_flipped = 0
        if not self.is_in_bounds(col, row):
            print("Flip Pieces bad params.")
            exit()
        for d in Direction:
            (next_col, next_row) = self.set_coords_in_direction(col,row,d)
            if self.check_endpoint(next_col, next_row, symbol, d, False):
                pieces_flipped += self.flip_pieces_helper(next_col, next_row, symbol, d)

        return pieces_flipped

    def has_legal_moves_remaining(self, symbol):
        for c in range (0, self.cols):
            for r in range (0, self.rows):
                if self.is_cell_empty(c, r) and self.is_legal_move(c, r, symbol):
                    return True
        return False

    def count_score(self, symbol):
        score = 0
        for c in range (0, self.cols):
            for r in range (0, self.rows):
                if self.grid[c][r] == symbol:
                    score+=1
        return score

    def play_move(self, col, row, symbol):
        self.set_cell(col, row, symbol)
        self.flip_pieces(col, row, symbol)

    def generate_legal_moves(self, symbol):
        # Generates legal move using has_legal_moves_remaining logic
        for c in range(0, self.cols):
            for r in range(0, self.rows):
                if self.is_cell_empty(c, r) and self.is_legal_move(c, r, symbol):
                    yield c, r

    def mobility(self):
        """
        Returns the mobility heuristic for a state
        Based off of pseudocode in research paper "An Analysis of Heuristics in Othello"
        by Vaishnavi Sannidhanam and Muthukaruppan Annamalai, at https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
        """
        max_moves = len(list(self.generate_legal_moves(self.p1_symbol)))
        min_moves = len(list(self.generate_legal_moves(self.p2_symbol)))
        if max_moves + min_moves != 0:
            mobility = 100 * (max_moves - min_moves) / (max_moves + min_moves)
        else:
            mobility = 0
        return mobility

    def corners_captured(self):
        """
        Returns the corners captured heuristic for a state
        Based off of pseudocode in research paper "An Analysis of Heuristics in Othello"
        by Vaishnavi Sannidhanam and Muthukaruppan Annamalai, at https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
        """
        corners = [[0, 0], [0, self.cols - 1], [self.rows - 1, 0], [self.rows - 1, self.cols - 1]]
        max_corners = 0
        min_corners = 0
        for c, r in corners:
            if self.get_cell(c, r) == self.p1_symbol:
                max_corners += 1
            elif self.get_cell(c, r) == self.p2_symbol:
                min_corners += 1
        if max_corners + min_corners != 0:
            corner_score = 100 * (max_corners - min_corners) / (max_corners + min_corners)
        else: 
            corner_score = 0
        return corner_score

    def heuristic(self):
        """
        Returns the heuristic for a state
        Based off of pseudocode in research paper "An Analysis of Heuristics in Othello"
        by Vaishnavi Sannidhanam and Muthukaruppan Annamalai, at https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
        """
        return self.mobility() + self.corners_captured()

    def isCutoff(self, symbol, start_time):
        """
        Returns true if the search should be cut off
        Cutoff time is 10 seconds, based on project analysis requirements
        """
        if not self.has_legal_moves_remaining(symbol):
            return True
        if time() - start_time > 10:
            return True
        return False
