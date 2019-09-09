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
            bomb_board (2D np arr): array of booleans, True signifies a bomb. (n+2) x (n+2)
            neighbours_board (2D np arr): array storing the information of adjacent bombs. (n+2) x (n+2)
            cell_board (2D list): list of Cell objects from class
            display (2D list): game display for playing in terminal
        """

        self._size = size
        self._bombs = bombs
        self.remaining = bombs
        self.cell_board = [[Cell(0) for i in range(self._size)] for j in range(self._size)]
        self.play = True

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

            if init_row <= ind1 <= init_row + 1 and init_col <= ind2 <= init_col + 1:
                continue

            elif not self.cell_board[ind1][ind2].bomb():
                self.cell_board[ind1][ind2].set_bomb()
                num_bombs += 1

        for i in range(self._size):
            for j in range(self._size):
                if self.cell_board[i][j].bomb():
                    self.on_neighbours(i, j, self.increment_val)

    def print_board(self):
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
        Increments the value of the cell by 1
        """
        self.cell_board[row][col].set_value(self.cell_board[row][col].value() + 1)

    def on_neighbours(self, row, col, func):
        """
        Args:
            row (int): row index
            col (int): col index
            func (function): any function that acts on specific coordinates

        Applies func on all neighbours
        """
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < self._size and 0 <= j < self._size:
                    func(i, j)

    def generate(self, init_row, init_col):
        """
        Creates board attributes, opens initial board
        Args:
            init_row (int): initial row that is opened
            init_col (int): initial column that is opened
        """

        self.open_cell(init_row, init_col)

    def open_cell(self, row, col):
        """
        Args:
            col (int)
            row (int)

        Handles opening cells using the Cell object, with flooding condition
        """

        cell = self.cell_board[row][col]

        if not cell.opened() and not cell.flagged() and 0 <= row < self._size and 0 <= col < self._size:
            cell.open()

            if cell.bomb():
                self.play = False

            # recursion
            if cell.value() == 0:
                self.on_neighbours(row, col, self.open_cell)

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

        if adj_flags == self.cell_board[row][col].value():

            self.on_neighbours(row, col, self.open_cell)

    def display(self):
        print("    " + " ".join([str(x) for x in range(self._size)]))
        for i in range(self._size):
            rows = []
            for j in range(self._size):
                cell = self.cell_board[i][j]
                if cell.opened():
                    if cell.bomb():
                        rows.append('!')
                    else:
                        rows.append(str(cell[i][j].value()))
                elif cell.flagged():
                    rows.append('X')

                elif not cell.flagged():
                    rows.append('_')

            print("{} | {}".format(i, " ".join(rows)))

    def size(self):
        return self._size

    def bombs(self):
        return self._bombs


if __name__ == "__main__":

    game = Board()

    game.create_board(3, 3)

    game.print_board()

    game.display()




