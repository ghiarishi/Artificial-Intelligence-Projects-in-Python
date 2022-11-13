############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import copy
import math

############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    print(n)
    return (math.factorial(n**2))/(math.factorial(n)*math.factorial(n**2-n)) 

def num_placements_one_per_row(n):
    print(n)
    return n**n

def n_queens_valid(board):
    if board is None:
        return False
    for i in range(len(board)):
        if board.count(board[i]) > 1:
          return False
        for j in range(len(board)):
            if i == j:
                continue
            if abs(i-j) == abs(board[i]-board[j]):
                return False
    return True

def dfs(n, board, solutions):
    if len(board) == n: # if the board is full
        solutions.append(board) # return it
        return
    for i in range(n): # check all n possible columns to place
        new_b = board + [i] # new board with the new queen
        if n_queens_valid(new_b): # check if the new board is valid
            dfs(n, new_b, solutions) # if it is valid, but NOT full, do more DFS
    return solutions

def n_queens_solutions(n):
    board = []
    solutions = dfs(n, board,[])
    return solutions

############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.rows = len(self.board)
        self.cols = len(self.board[0])
        self.moves = []

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        board = self.board
        board[row][col] = not board[row][col]
        if row-1 >= 0:
            board[row-1][col] = not board[row-1][col]
        if col-1>= 0:
            board[row][col-1] = not board[row][col-1]
        if row+1 <= self.rows-1:
            board[row+1][col] = not board[row+1][col]
        if col+1 <= self.cols-1: 
            board[row][col+1] = not board[row][col+1]
        self.board = board
                    
    def scramble(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if random.random() < 0.5:
                    self.perform_move(i,j)

    def is_solved(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j]:
                    return False
        return True

    def copy(self):
        return LightsOutPuzzle(copy.deepcopy(self.board))

    def successors(self):
        for i in range(self.rows):
            for j in range(self.cols):
                puzzle = self.copy()
                puzzle.perform_move(i,j)
                yield (i,j),puzzle

    def find_solution(self):
        queue = [] # queue of all unvisited instances of the puzzle
        queue.append(self) 
        visited = set()
        board_prev = tuple([tuple(row) for row in self.get_board()])
        visited.add(board_prev)
        if self.is_solved():
            return []
        while len(queue) > 0: # while the queue isn't empty
            for move, new_p in queue[0].successors(): # pop off the first element of the queue, and iterate through its successors
                for i in range(len(queue[0].moves)):
                    new_p.moves.append(queue[0].moves[i])
                new_p.moves.append(move) # append the move made to get to that successor to the puzzle
                if new_p.is_solved(): # check if the successors are solved. If one of them is, then do the following
                    return new_p.moves # return that set of moves
                board_prev = tuple([tuple(row) for row in new_p.get_board()])
                if board_prev not in visited:
                    queue.append(new_p) # if not solved, just add it to the queue
                    visited.add(board_prev)
            queue.pop(0) # remove the front element of the queue, whose children we have checked already
        return None

def create_puzzle(rows, cols):
    big_list = []
    for i in range(rows): 
        list = []
        for j in range(cols):
             list.append(False) 
        big_list.append(list)
    return LightsOutPuzzle(big_list)

############################################################
# Section 3: Linear Disk Movement
############################################################
class Disk(object):

    def __init__(self, n, length, disks):
        self.disks = disks
        self.length = length
        self.n = n
        self.moves = []

    def perform_move(self, p, q):
        self.disks[q] = self.disks[p]
        self.disks[p] = 0 

    def get_list(self):
        return self.disks
        
    def copy(self):
        return Disk(self.n, self.length, copy.deepcopy(self.disks))

    def successors(self):
        for p in range(self.length):
            if self.disks[p] > 0:
                if p+2 < self.length and self.disks[p+1] > 0 and self.disks[p+2] == 0:
                    new_p = self.copy()
                    new_p.perform_move(p, p+2)
                    yield ((p, p+2), new_p)
                if p+1 < self.length and self.disks[p+1] == 0:
                    new_p = self.copy()
                    new_p.perform_move(p, p+1)
                    yield ((p, p+1), new_p)
                if p-1 >= 0 and self.disks[p-1] == 0:
                    new_p = self.copy()
                    new_p.perform_move(p, p-1)
                    yield ((p, p-1), new_p)
                if p-2 >= 0 and self.disks[p-1] > 0 and self.disks[p-2] == 0:
                    new_p = self.copy()
                    new_p.perform_move(p, p-2)
                    yield ((p, p-2), new_p)

    def successors_distinct(self):
        for p in range(self.length):
            if self.disks[p] > 0:
                if p+2 < self.length and self.disks[p+1] > 0 and self.disks[p+2] == 0:
                    new_p = self.copy()
                    new_p.perform_move(p, p+2)
                    yield ((p, p+2), new_p)
                if p+1 < self.length and self.disks[p+1] == 0:
                    new_p = self.copy()
                    new_p.perform_move(p, p+1)
                    yield ((p, p+1), new_p)
                if p-1 >= 0 and self.disks[p-1] == 0:
                    new_p = self.copy()
                    new_p.perform_move(p, p-1)
                    yield ((p, p-1), new_p)
                if p-2 >= 0 and self.disks[p-1] > 0 and self.disks[p-2] == 0:
                    new_p = self.copy()
                    new_p.perform_move(p, p-2)
                    yield ((p, p-2), new_p)

    def is_solved(self):
        part1 = self.disks[:(self.length - self.n)]
        part2 = self.disks[(self.length - self.n + 1):self.length]

        if self.disks.count(0) != self.length - self.n:
            return False

        if part1.count(0) == (self.length - self.n) and part2.count(0) == 0:
            return True
        return False
    
    def is_solved_distinct(self):
        if not self.is_solved():
            return False
        for i in range(self.length):
            if i < self.length-self.n:
                continue
            if self.disks[i] < self.disks[i-1]:
                return False
        return True
                    
    def find_solution(self):
        queue = [] 
        queue.append(self) 
        visited = set()
        disks_prev = tuple(self.get_list())
        visited.add(disks_prev)
        if self.is_solved():
            return []

        while len(queue) > 0: 

            # SUCCESSORS ARE CHECKED
            for move, new_d in queue[0].successors(): 

                new_d_tup = tuple(new_d.get_list())

                # PAST VISITATION IS CHECKED
                if new_d_tup not in visited:
                    visited.add(new_d_tup)

                    # MOVES ARE APPENDEaZD TO NEW_D
                    for i in range(len(queue[0].moves)):
                        new_d.moves.append(queue[0].moves[i])
                    new_d.moves.append(move) 

                    # IS THE NEW_D SOLVED? IF YES, RETURN ITS MOVES
                    if new_d.is_solved():
                        return new_d.moves 

                    # ADD THE NEW_D TO Q IF NOT VISITED AND NOT SOLVED
                    queue.append(new_d) 

                # IF VISITED, MOVE ON TO THE NEXT NEW_D WITHOUT DOING ANYTHING
            
            # POP OFF THE FIRST ELEMENT OF QUEUE ONCE ALL ITS CHILDREN ARE CHECKED
            queue.pop(0) 
        return None

    def find_solution_distinct(self):
        queue = [] 
        queue.append(self) 
        visited = set()
        disks_prev = tuple(self.get_list())
        visited.add(disks_prev)
        if self.is_solved():
            return []

        while len(queue) > 0: 

            # SUCCESSORS ARE CHECKED
            for move, new_d in queue[0].successors_distinct(): 
                new_d_tup = tuple(new_d.get_list())

                # PAST VISITATION IS CHECKED
                if new_d_tup not in visited:
                    visited.add(new_d_tup)

                    # MOVES ARE APPENDEaZD TO NEW_D
                    for i in range(len(queue[0].moves)):
                        new_d.moves.append(queue[0].moves[i])
                    new_d.moves.append(move) 

                    # IS THE NEW_D SOLVED? IF YES, RETURN ITS MOVES
                    if new_d.is_solved_distinct():
                        return new_d.moves 

                    # ADD THE NEW_D TO Q IF NOT VISITED AND NOT SOLVED
                    queue.append(new_d) 

                # IF VISITED, MOVE ON TO THE NEXT NEW_D WITHOUT DOING ANYTHING
            
            # POP OFF THE FIRST ELEMENT OF QUEUE ONCE ALL ITS CHILDREN ARE CHECKED
            queue.pop(0) 
        return None

def solve_identical_disks(length, n):
    disks = []
    for i in range(length):
        if i < n:
            disks.append(1)
        else: 
            disks.append(0) 
    d = Disk(n, length, disks)
    solution = d.find_solution()
    return solution


def solve_distinct_disks(length, n):
    print(length, n)
    disks = []
    for i in range(length):
        if i < n:
            disks.append(n-i)
        else: 
            disks.append(0) 
    d = Disk(n, length, disks)
    solution = d.find_solution_distinct()
    return solution

