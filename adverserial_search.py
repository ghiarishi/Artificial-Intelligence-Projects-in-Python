
############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import collections
import copy
import itertools
import random
import math

############################################################
# Section 1: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    board = []
    for i in range(rows):
        row = []
        for j in range (cols):
            row.append(False)
        board.append(row)
    return DominoesGame(board)

class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.move = (0,0)
        self.leaves = 0
        self.depth = 0

    def get_board(self):
        return self.board

    def reset(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = False

    def is_legal_move(self, row, col, vertical):
        if vertical:
            if row + 1 >= self.rows:
                return False
            return (self.board[row][col] == False and self.board[row+1][col] == False)
        else:
            if col + 1 >= self.cols:
                return False
            return (self.board[row][col] == False and self.board[row][col+1] == False)    

    def legal_moves(self, vertical):
        for i in range(self.rows):
            if vertical and i == self.rows:
                continue
            for j in range(self.cols):
                if not vertical and j == self.cols: 
                    continue
                if self.is_legal_move(i, j, vertical):
                    yield (i, j)

    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row, col, vertical):
            self.board[row][col] = True
            if vertical:   
                self.board[row+1][col] = True
            else: 
                self.board[row][col+1] = True

    def game_over(self, vertical):
        if len(list(self.legal_moves(vertical))) == 0:
            return True
        return False

    def copy(self):
        return DominoesGame(copy.deepcopy(self.board))

    def successors(self, vertical):
        for move in self.legal_moves(vertical):
            game = self.copy()
            game.perform_move(move[0], move[1], vertical)
            yield move, game

    def get_random_move(self, vertical):
        return random.choice(self.legal_moves(vertical))

    def max_value(self, vertical, limit, a, b, root):
        # difference in num of possible legal moves of current and other player
        if self.game_over(vertical) or limit == 0:
            root.leaves += 1
            return len(list(self.legal_moves(vertical))) - len(list(self.legal_moves(not vertical))) 
        v = -math.inf
        for move, child in self.successors(vertical):
            v_prime = child.min_value(not vertical, limit-1, a, b, root)          
            if v_prime > v:
                v = v_prime
                if root.depth - limit + 1 == 1:
                    root.move = move
            if v >= b:
                return v
            if v > a:
                a = v
        return v

    def min_value(self, vertical, limit, a, b, root):
        # difference in num of possible legal moves of current and other player
        if self.game_over(vertical) or limit == 0:
            root.leaves += 1
            return len(list(self.legal_moves(not vertical))) - len(list(self.legal_moves(vertical))) 
        v = math.inf
        for move, child in self.successors(vertical):
            v_prime = child.max_value(not vertical, limit-1, a, b, root)          
            if v_prime < v:
                v = v_prime
                
            if v <= a: 
                return v
            if v < b:
                b = v
        return v

    # Required
    def get_best_move(self, vertical, limit):
        a = -math.inf
        b = math.inf
        root = self
        root.depth = limit
        value = self.max_value(vertical, limit, a, b, root)

        return root.move, value, root.leaves

