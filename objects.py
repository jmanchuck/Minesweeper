# minesweeper by jmc

import numpy as np


class Cell:
    def __init__(self, value, bomb=False, opened=False, flagged=False):
        """
        Args:
            value (int): number of surrounding bombs
            bomb (bool): bomb or not
            opened (bool): opened or not
            flagged (bool): flagged or not
        """
        self._opened = opened
        self._flagged = flagged
        self._value = value
        self._bomb = bomb

    def open(self):  # when mouse click occurs to open, change cell state to opened
        self._opened = True

    def flag(self):  # when mouse click for flag, change cell state to flagged
        self._flagged = True

    def unflag(self):
        self._flagged = False

    def opened(self):
        return self._opened

    def flagged(self):
        return self._flagged

    def bomb(self):
        return self._bomb

    def value(self):
        return self._value

    def set_value(self, val):
        self._value = val

    def set_bomb(self):
        self._bomb = True


class Board:
    def __init__(self, size=10, bombs=25):

        """
        Args:
            size (int): integer n for dimension n x n of square array (maybe change or extend to rectangle)
            bombs (int): number of bombs on the board (must be less than size^2)

        Attributes:
            cell_board (2D list): list of Cell objects from class
            size (int): size of board n (n x n)
            bombs (int): number of remaining bombs
            remaining (int): keeps track of how many bombs remaining
            num_open (int): keeps track of how many cells opened
        """

        self._size = size
        self._bombs = bombs
        self._remaining = bombs
        self._num_open = 0
        self.cell_board = [[Cell(0) for i in range(self._size)] for j in range(self._size)]
        self.play = True

    def create_threes(self, init_row, init_col):
        """

        Args:
            init_row: initial opened row
            init_col: initial opened column

        Use for testing solver on a 3x3 sized game

        """
        # randomly place bombs
        num_bombs = 0

        while num_bombs < self._bombs:
            ind1 = np.random.randint(self._size)
            ind2 = np.random.randint(self._size)

            if init_row == ind1 and init_col == ind2:
                continue

            elif not self.cell_board[ind1][ind2].bomb():
                self.cell_board[ind1][ind2].set_bomb()
                num_bombs += 1

        for i in range(self._size):
            for j in range(self._size):
                if self.cell_board[i][j].bomb():
                    self.on_neighbours(i, j, self.increment_val)

        self.open_cell(init_row, init_col)

    def create_board(self, init_row, init_col):
        """
        Args:
            init_col (int): initial col selection
            init_row (int): initial row selection, ensures there is no bomb on first selection
        """

        # randomly place bombs
        num_bombs = 0

        while num_bombs < self._bombs:
            ind1 = np.random.randint(self._size)
            ind2 = np.random.randint(self._size)

            if init_row - 1 <= ind1 <= init_row + 1 and init_col - 1 <= ind2 <= init_col + 1:
                continue

            elif not self.cell_board[ind1][ind2].bomb():
                self.cell_board[ind1][ind2].set_bomb()
                num_bombs += 1

        for i in range(self._size):
            for j in range(self._size):
                if self.cell_board[i][j].bomb():
                    self.on_neighbours(i, j, self.increment_val)

        self.open_cell(init_row, init_col)

    def print_board(self):
        """
        Prints the answers
        """
        for i in range(self._size):
            row = []
            for j in range(self._size):
                if self.cell_board[i][j].bomb():
                    row.append("!")
                else:
                    row.append(str(self.cell_board[i][j].value()))
            print(" ".join(row))

    def increment_val(self, row, col):
        """
        Args:
            row:
            col:
        Increments the value of a cell at row, col by 1
        """
        self.cell_board[row][col].set_value(self.cell_board[row][col].value() + 1)

    def on_neighbours(self, row, col, func):
        """
        Args:
            row (int): row index
            col (int): col index
            func (function): any function that acts on specific coordinates

        Applies func on all neighbours of row and col
        """
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < self._size and 0 <= j < self._size:
                    func(i, j)

    def open_cell(self, row, col):
        """
        Args:
            col (int)
            row (int)

        Handles opening cells using the Cell object, with flooding condition
        """

        cell = self.cell_board[row][col]

        if not cell.flagged() and 0 <= row < self._size and 0 <= col < self._size:
            if not cell.opened():
                cell.open()
                self._num_open += 1

                if cell.bomb():
                    self.play = False

                # recursion
                if cell.value() == 0:
                    self.on_neighbours(row, col, self.open_cell)

    def flag_cell(self, row, col):
        """
        Args:
            row:
            col:

        Flags or unflags cell depending on state
        """
        if self.cell_board[row][col].flagged():
            self.cell_board[row][col].unflag()
            self._remaining += 1
        else:
            self.cell_board[row][col].flag()
            self._remaining -= 1

    def open_neighbours(self, row, col):
        """
        Args:
            col (int)
            row (int)

        Auto opens neighbours for a cell that is open and has number of surrounding flags = cell's value
        Note that if the flags are wrong, the player loses by opening a bomb
        """
        adj_flags = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < self._size and 0 <= j < self._size:
                    if self.cell_board[i][j].flagged():
                        adj_flags += 1

        if adj_flags == self.cell_board[row][col].value() and adj_flags > 0:
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < self._size and 0 <= j < self._size:
                        self.open_cell(i, j)

    def display(self):
        """
        Displays a playable array in terminal
        """
        print("    " + " ".join([str(x) for x in range(self._size)]))
        for i in range(self._size):
            rows = []
            for j in range(self._size):
                cell = self.cell_board[i][j]
                if cell.opened():
                    if cell.bomb():
                        rows.append('!')
                    else:
                        rows.append(str(cell.value()))
                elif cell.flagged():
                    rows.append('X')

                elif not cell.flagged():
                    rows.append('_')

            print("{} | {}".format(i, " ".join(rows)))

    def get_arr(self):
        return self.cell_board

    def size(self):
        return self._size

    def bombs(self):
        return self._bombs

    def remaining(self):
        return self._remaining

    def num_open(self):
        return self._num_open


if __name__ == "__main__":

    game = Board()
    game.create_board(3, 3)
    game.print_board()

    game.display()

    i = 0
    tests = 20

    board = game.cell_board

    # 100 loops for testing
    while i < 100 and game.play:

        if i % 2 == 0:
            print("open something")
            row = int(input("row: "))
            col = int(input("col: "))
            if board[row][col].opened():
                game.open_neighbours(row, col)
            game.open_cell(row, col)
        else:
            print("flag something")
            row = int(input("row: "))
            col = int(input("col: "))
            game.flag_cell(row, col)
        i += 1
        game.display()
