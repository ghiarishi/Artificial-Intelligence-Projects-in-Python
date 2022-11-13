############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import copy

############################################################
# Section 1: Sudoku Solver
############################################################

def sudoku_cells():
    list = []
    for i in range(9):
        for j in range(9):
            list.append((i,j))
    return list

def sudoku_arcs():
    arcs = []
    cells = sudoku_cells()
    for i in cells:
        for j in cells: 
            if i == j:
                continue
            if i[0] == j[0] or i[1] == j[1]:
                arcs.append((i, j))
                continue
            for x in range(0, 9, 3):
                for y in range(0, 9, 3):
                    if (x <= i[0] < x + 3) and (x <= j[0] < x + 3) and (y <= i[1] < y + 3) and (y <= j[1] < y + 3):
                        arcs.append((i, j))
    return arcs
                
def read_board(path):
    print(path) # REMOVE 
    file1 = open(path, 'r')
    lines = file1.readlines()
    board = {}
    i = 0
    j = 0
    for line in lines: 
        for num in line: 
            if num == '*':
                board[(i,j)] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            elif num == '\n':
                continue
            else:
                board[(i,j)] = {int(num)}
            j += 1
        i += 1
        j = 0    
    return board

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board
        self.n = 9

    def get_values(self, cell):
        return self.board.get(cell)

    def remove_inconsistent_values(self, cell1, cell2):
        if (cell1, cell2) in Sudoku.ARCS: 
            if len(self.board.get(cell2)) > 1 or len(self.board.get(cell1)) == 1:
                return False
            cell2_set = self.board.get(cell2)
            for num in cell2_set:
                if num in self.board.get(cell1):
                    self.board.get(cell1).remove(num)
                return True
            else:
                return False

    def infer_ac3(self):
        queue = []
        for item in Sudoku.ARCS:
            queue.append(item)
        while len(queue) != 0:
            arc = queue.pop(0)
            if self.remove_inconsistent_values(arc[0], arc[1]):
                for arcs in Sudoku.ARCS:
                    if (arcs[0] == arc[0]) and (arcs[1] != arc[1]):
                        queue.append((arcs[1], arcs[0]))

    def infer_improved(self):
        extra_inference = True
        while extra_inference:
            self.infer_ac3()
            extra_inference = False
            for cell in Sudoku.CELLS: # check each cell
                if len(self.board.get(cell)) > 1: # if there is more than 1 value possible
                    for val in self.board.get(cell): # check for each value in the possible ones

                        val_unique = True

                        x = cell[0]
                        y = cell[1]

                        # check the row
                        for i in range(9):
                            if val in self.board.get((i, y)) and (i,y)!= cell:
                                val_unique = False
                                break

                        if val_unique: 
                            extra_inference = True
                            self.board[cell] = {val}
                            break

                        # check the col
                        for j in range(9):
                            if val in self.board.get((x, j)) and (x, j)!= cell:
                                val_unique = False
                                break

                        if val_unique: 
                            extra_inference = True
                            self.board[cell] = {val}
                            break

                        # check the subgrid     
                        grid_x = (cell[0]//3)*3 
                        grid_y = (cell[1]//3)*3 

                        for i in range(3):
                            for j in range(3):
                                if (val in self.board.get((grid_x + i, grid_y + j))) and (grid_x + i, grid_y + j) != cell:
                                    val_unique = False
                                    break
                        
                        if val_unique: 
                            extra_inference = True
                            self.board[cell] = {val}
                            break

    def infer_with_guessing(self):

        if self.is_solved(): # do nothing
            return self.board

        self.infer_improved() # do as much as possible through infer

        for cell in self.CELLS: # check each cell

                if len(self.board.get(cell)) > 1:

                    for val in self.board.get(cell):

                        board_with_guess = copy.deepcopy(self.board)
                        self.board[cell] = {val}
                        self.infer_with_guessing() # recursive call

                        if self.is_solved():
                            break
                        else:       
                            self.board = board_with_guess # if not solved, continue with new board
                    return
    
    # check if the board is solved 
    def is_solved(self):

        # matrix with true and false to indicate whether a cell value is final or not final
        check = []
        n = 9
        for i in range(3*n):
            lst = []
            for j in range(n):
                lst.append(False)
            check.append(lst)

        for cell in self.CELLS:

            if (len(self.board.get(cell)) > 1) or (len(self.board.get(cell)) < 1):
                return False    

            for val in self.board.get(cell):
                x = cell[0]
                y = cell[1]

                x_grid = x//3
                y_grid = y//3
                
                check[x][val-1] = True
                check[n + y][val-1] = True
                check[(x_grid * 3) + y_grid + 2*n ][val-1] = True

        # implement the check, returning false if there is a cell with NOT ONE value, or isnt matching the check matrix
        for i in range(3*n):
            for j in range(n):
                if not check[i][j]:
                    return check[i][j]
        return True
