############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import copy
from queue import PriorityQueue 
import math


############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    board = []
    for row in range(rows):
        c = []
        for col in range(cols):
            c.append((row * cols) + col + 1)
        board.append(c)
    board[-1][-1] = 0  # set the last lower right corner of board to 0 (empty)
    return TilePuzzle(board)


class TilePuzzle(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.r = len(board)  # rows
        self.c = len(board[0])  # columns
        for i in range(self.r):
            for j in range(self.c):
                if self.board[i][j] == 0:
                    self.empty_col = j
                    self.empty_row = i

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        if direction == 'up':
            if self.empty_row - 1 >= 0:
                self.board[self.empty_row][self.empty_col] = self.board[self.empty_row - 1][self.empty_col]
                self.board[self.empty_row - 1][self.empty_col] = 0
                self.empty_row -= 1
                return True

        elif direction == 'right':
            if self.empty_col + 1 <= self.c - 1:
                self.board[self.empty_row][self.empty_col] = self.board[self.empty_row][self.empty_col + 1]
                self.board[self.empty_row][self.empty_col + 1] = 0
                self.empty_col += 1
                return True

        elif direction == 'down':
            if self.empty_row + 1 <= self.r - 1:
                self.board[self.empty_row][self.empty_col] = self.board[self.empty_row + 1][self.empty_col]
                self.board[self.empty_row + 1][self.empty_col] = 0
                self.empty_row += 1
                return True

        elif direction == 'left':
            if self.empty_col - 1 >= 0:
                self.board[self.empty_row][self.empty_col] = self.board[self.empty_row][self.empty_col - 1]
                self.board[self.empty_row][self.empty_col - 1] = 0
                self.empty_col -= 1
                return True

        return False

    def scramble(self, num_moves):
        for i in range(num_moves):
            direction = random.choice(['up', 'down', 'left', 'right'])
            self.perform_move(direction)

    def is_solved(self):
        if self.board[-1][-1] != 0:
            return False
        count = 1
        for row in range(self.r):
            for col in range(self.c):
                if (self.board[row][col] != count) and (count != self.r*self.c):
                    return False
                count += 1
        return True

    def copy(self):
        return TilePuzzle(copy.deepcopy(self.board))

    def successors(self):
        iter_up = self.copy()
        iter_down = self.copy()
        iter_left = self.copy()
        iter_right = self.copy()

        if iter_up.perform_move('up'):
            yield 'up', iter_up
        if iter_down.perform_move('down'):
            yield 'down', iter_down
        if iter_left.perform_move('left'):
            yield 'left', iter_left
        if iter_right.perform_move('right'):
            yield 'right', iter_right

    def find_solutions_iddfs(self):
        if self.is_solved():
            yield []
            return

        depth = 0

        solved = False

        while not solved:
            # check all puzzles at a certain depth, and if they're solved, do NOT go beyond that depth
            for moves, puzzle in self.iddfs_helper(depth, []):
                if puzzle.is_solved():
                    solved = True
                    yield moves
            # but if none of them ar solved, just return
            depth += 1

    def iddfs_helper(self, depth_remaining, moves):
        if depth_remaining <= 0:
            yield moves, self
            return
        depth_remaining -= 1

        for move, puzzle in self.successors():
            new_moves = moves + [move]
            if puzzle.is_solved():
                yield new_moves, puzzle
            else:
                for moves_made, puzzles in puzzle.iddfs_helper(depth_remaining, new_moves):
                    yield moves_made, puzzles

    def heuristic_calc(self):
        heuristic_val = 0
        n1 = self.r
        n2 = self.c
        for row in range(n1):
            for col in range(n2):
                if self.board[row][col] != 0:
                    heuristic_val += abs(row - (self.board[row][col]-1) // n1) + abs(col - (self.board[row][col]-1) % n2)
        return heuristic_val

    # Required
    def find_solution_a_star(self):

        frontier = PriorityQueue()
        cost = 0
        moves = []
        solved = False

        # add the base vertex to the frontier
        frontier.put((self.heuristic_calc(), cost, moves, self))

        # maintain set of visited vertices
        # where a vertex is a puzzle state
        visited = set()               

        while not solved:

            # dequeue the highest priority (lowest cost) vertex 
            vertex = frontier.get()  
            
            tup = tuple(tuple(item) for item in vertex[3].board)

            # if the vertex has already been visited, ignore it and dequeue the next element
            if tup in visited:    
                continue
            
            # if not visited previously, add the vertex to the set of visited elements
            else:
                visited.add(tup)  
            
            # if the vertex's board is solved, the optimal solution has been found. Return the moves. 
            if vertex[3].is_solved(): 
                solved = True
                return vertex[2]

            # if not solved, find all the children to the current vertex/board    
            for (move, puzzle) in vertex[3].successors():

                # if the children have NOT been visited in the past, then queue them onto the frontier
                if tuple(tuple(item) for item in puzzle.board) not in visited:
                    frontier.put((vertex[1] + 1 + puzzle.heuristic_calc(), vertex[1] + 1, vertex[2] + [move], puzzle))

############################################################
# Section 2: Grid Navigation
############################################################

class GridNav(object):

    def __init__(self, start, goal, scene):
        self.scene = scene
        self.goal = goal
        self.loc = start # current location
        self.r = len(scene)  # rows
        self.c = len(scene[0])  # columns
       
    def get_scene(self):
        return self.scene

    def perform_move(self, direction):

        if direction == "up":
            if self.loc[0] > 0:
                if self.scene[self.loc[0] - 1][self.loc[1]] is False:
                    self.loc = (self.loc[0] - 1, self.loc[1])
                    return True

        if direction == "down":
            if self.loc[0] < self.r - 1:
                if self.scene[self.loc[0] + 1][self.loc[1]] is False:
                    self.loc = (self.loc[0] + 1, self.loc[1])
                    return True

        if direction == "left":
            if self.loc[1] > 0:
                if self.scene[self.loc[0]][self.loc[1] - 1] is False:
                    self.loc = (self.loc[0], self.loc[1] - 1)
                    return True

        if direction == "right":
            if self.loc[1] < self.c - 1:
                if self.scene[self.loc[0]][self.loc[1] + 1] is False:
                    self.loc = (self.loc[0], self.loc[1] + 1)
                    return True

        if direction == "up-left":
            if self.loc[0] > 0:
                if self.loc[1] > 0:
                    if self.scene[self.loc[0] - 1][self.loc[1] - 1] is False:
                        self.loc = (self.loc[0] - 1, self.loc[1] - 1)
                        return True

        if direction == "up-right":
            if self.loc[0] > 0:
                if self.loc[1] < self.c - 1:
                 if self.scene[self.loc[0] - 1][self.loc[1] + 1] is False:
                    self.loc = (self.loc[0] - 1, self.loc[1] + 1)
                    return True

        if direction == "down-left":
            if self.loc[0] < self.r - 1:
                if self.loc[1] > 0:
                    if self.scene[self.loc[0] + 1][self.loc[1] - 1] is False:
                        self.loc = (self.loc[0] + 1, self.loc[1] - 1)
                        return True

        if direction == "down-right":
            if self.loc[0] < self.r - 1:
                if self.loc[1] < self.c - 1:
                    if self.scene[self.loc[0] + 1][self.loc[1] + 1] is False:
                        self.loc = (self.loc[0] + 1, self.loc[1] + 1)
                        return True        
        return False

    def is_solved(self):
        return self.loc == self.goal

    def copy(self):
        return GridNav(copy.copy(self.loc), copy.copy(self.goal), copy.copy(self.scene))

    def successors(self):
        iter_up = self.copy()
        iter_down = self.copy()
        iter_left = self.copy()
        iter_right = self.copy()
        iter_downright = self.copy()
        iter_upright = self.copy()
        iter_downleft = self.copy()
        iter_upleft = self.copy()

        if iter_up.perform_move('up'):
            yield 'up', iter_up.loc, iter_up
        if iter_down.perform_move('down'):
            yield 'down', iter_down.loc, iter_down
        if iter_left.perform_move('left'):
            yield 'left', iter_left.loc, iter_left
        if iter_right.perform_move('right'):
            yield 'right', iter_right.loc, iter_right
        if iter_upleft.perform_move('up-left'):
            yield 'up-left', iter_upleft.loc, iter_upleft
        if iter_upright.perform_move('up-right'):
            yield 'up-right', iter_upright.loc, iter_upright
        if iter_downleft.perform_move('down-left'):
            yield 'down-left', iter_downleft.loc, iter_downleft
        if iter_downright.perform_move('down-right'):
            yield 'down-right', iter_downright.loc, iter_downright

    def heuristic_calc(self):
        a = math.pow((self.loc[0] - self.goal[0]), 2)
        b = math.pow((self.loc[1] - self.goal[1]), 2)
        return (a+b)**0.5

def find_path(start, goal, scene):

    grid = GridNav(start, goal, scene)
    
    # if the starting location is blocked, return none (no soln)
    if grid.scene[grid.loc[0]][grid.loc[1]]:   
        return None

    frontier = PriorityQueue()

    # add the starting state to the frontier
    frontier.put((grid.heuristic_calc(), 0, [grid.loc], grid))  

    visited = set()               

    while not frontier.empty():

        # dequeue the higher priority vertex
        vertex = frontier.get()     

        # if solved, return the moves
        if vertex[3].is_solved(): 
            return vertex[2]

        # if the vertex has been visited, ignore it | if not visited before, mark it as visited   
        if vertex[3].loc not in visited:    
            visited.add(vertex[3].loc)
        else:
            continue

        # iterate through the children of the vertex 
        for (direction, location, puzzle) in vertex[3].successors():

            # check them further only if not visited prior
            if location in visited: 
                continue   

            else: 
                # cost of these is 1 (euclidean), so add 1 to the cost
                if direction in ["up", "left", "down", "right"]:    
                    frontier.put((vertex[1] + 1 + puzzle.heuristic_calc(), vertex[1] + 1, vertex[2] + [location], puzzle))
                
                # cost of these is sqrt(2) (euclidean), so add 1.414 to the cost
                elif direction in ["up-left", "up-right", "down-left", "down-right"]:
                    frontier.put((vertex[1] + 1.4142135 + puzzle.heuristic_calc(), vertex[1] + 1.4142135, vertex[2] + [location], puzzle))
                    
                else:
                    return None

    # if the queue is empty, there are no more unvisited states left. hence no solution. return none
    return None

############################################################
# Section 3: Linear Disk Movement, Revisited
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
        return Disk(self.n, self.length, copy.copy(self.disks))

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

    def heuristic_calc(self):
        heuristic = 0
        for num in range(self.length):
            if self.disks[num] != -1:
                heuristic += abs(self.length - self.disks[num] - num - 1)
        return heuristic

    def find_solution_a_star(self):

        frontier = PriorityQueue()

        frontier.put((self.heuristic_calc(), 0, [], self))  

        # set of visited elements
        visited = set()               

        # while the priority queue is not empty, run, else return none
        while not frontier.empty():

            vertex = frontier.get()

            # return the moves if solved
            if vertex[3].is_solved_distinct(): 
                return vertex[2]
            
            # if visited already, do nothing, else add it to visited
            if tuple(vertex[3].disks) in visited:   
                continue
            else:
                visited.add(tuple(vertex[3].disks))  
            
            # iterate through the children of the current vertex, and add them to the PQ if they haven't been visited
            for (move, puzzle) in vertex[3].successors_distinct():
                if tuple(puzzle.disks) not in visited:
                    frontier.put((vertex[1] + 1 + puzzle.heuristic_calc(), vertex[1] + 1, vertex[2] + [move], puzzle))

        return None

def solve_distinct_disks(length, n):
    disks = []
    for i in range(length):
        if i < n:
            disks.append(n-i)
        else: 
            disks.append(0) 
    p = Disk(n, length, disks)
    return p.find_solution_a_star()
   
