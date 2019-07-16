import numpy as np


class Cell:
    def __init__(self, value=None, bomb=False, opened=False, flagged=False):
        """
        Args:
            value (int): number of surrounding bombs (will be displayed)

            bomb (bool): bomb or not

            opened (bool): opened or not

            flagged (bool): flagged or not
        """
        self._value = value
        self._bomb = bomb
        self._opened = opened
        self._flagged = flagged

    def open(self):  # when mouse click occurs to open, change cell state to opened
        self._opened = True

    def flag(self):  # when mouse click for flag, change cell state to flagged
        self._flagged = True

    def opened(self):
        return self._opened

    def value(self):
        return self._value

    def bomb(self):
        return self._bomb

    def flagged(self):
        return self._flagged


class Board:
    def __init__(self, size=8, bombs=24):
        
        """
        Args:
            size (int): integer n for dimension n x n of square array (maybe change or extend to rectangle)

            bombs (int): number of bombs on the board (must be less than size^2)

        Attributes:
            fake_bomb_board (2D np arr): array of booleans, True signifies a bomb. (n+2) x (n+2)

            bomb_board (2D np arr): same as above but without the extra 'False' surrounding it. n x n

            neighbours_board (2D np arr): array storing the information of adjacent bombs. n x n

            cell_board (2D list): list of Cell objects. Cell(value, bomb), default opened and flagged is False
        """
        
        self._size = size
        self._bombs = bombs
        self.fake_bomb_board = self.create_fake_bomb_board(input('initial column: '), input('initial row: '))
        self.bomb_board = self.create_bomb_board()
        self.neighbours_board = self.create_neighbours_board()
        self.cell_board = self.create_cell_board()
        self.display_board = np.zeros((self._size, self._size), dtype='O')

    def create_fake_bomb_board(self, init_col, init_row):
        """
        Args:
            init_col (int): initial col selection
            init_row (int): initial row selection, ensures there is no bomb on first selection
        Returns:
             (n+2) x (n+2) 2D boolean array of bombs
        """

        # create an extra perimeter with no bombs around the board for ease of checking neighbours
        board_array = np.zeros((self._size+2, self._size+2), dtype=bool)

        num_bombs = 0

        while num_bombs < self._bombs:
            ind1 = np.random.randint(1, self._size+1)
            ind2 = np.random.randint(1, self._size+1)

            if ind1 == init_row and ind2 == init_col:
                continue

            elif not board_array[ind1][ind2]:
                board_array[ind1][ind2] = True
                num_bombs += 1

        return board_array

    def print_fake_bomb_board(self):
        print(self.fake_bomb_board)

    def return_neighbour(self, col, row):
        """
        Args:
            col (int): column index
            row (int): row index
        Returns:
            number of bombs in immediate neighbour (max 8) for a specific position
            None if position is bomb
        """
        if self.fake_bomb_board[col][row]:
            return 0

        else:
            neighbours = 0

            for i in [col-1, col, col+1]:
                for j in [row-1, row, row+1]:
                    if i == col and j == row:
                        pass
                    else:
                        if self.fake_bomb_board[i][j]:
                            neighbours += 1

            return neighbours

    def create_neighbours_board(self):
        """
        Returns
            2D array storing how many neighbours are bombs
        """

        board = np.zeros((self._size, self._size))

        for i in range(self._size):
            for j in range(self._size):
                board[i][j] = self.return_neighbour(i+1, j+1)

        return board

    def print_neighbours_board(self):
        print(self.neighbours_board)

    def create_bomb_board(self):
        """
        Returns:
             n x n 2D boolean array of bombs
        """
        real_board = np.zeros((self._size, self._size), dtype=bool)

        for i in range(self._size):
            for j in range(self._size):
                real_board[i][j] = self.fake_bomb_board[i+1][j+1]

        return real_board
    
    def print_bomb_board(self):
        print(self.bomb_board)

    def create_cell_board(self):
        """
        Returns:
            2D list of Cell objects
        """
        bombs_board = self.bomb_board

        neighbour_board = self.neighbours_board

        cell_objects = [[None for x in range(self._size)] for x in range(self._size)]

        for i in range(self._size):
            for j in range(self._size):
                cell_objects[i][j] = Cell(neighbour_board[i][j], bombs_board[i][j])

        return cell_objects

    def print_display(self):
        print(self.display_board)

    def open_cell(self, col, row):
        self.cell_board[col][row].open()
        if self.cell_board[col][row].bomb():
            self.display_board[col][row] = '!'
        else:
            self.display_board[col][row] = self.cell_board[col][row].value()

    def flag_cell(self, col, row):
        self.cell_board[col][row].flag()

        self.display_board[col][row] = 'X'

    def size(self):
        return self._size

    def bombs(self):
        return self._bombs


if __name__ == "__main__":
    game = Board()
    # game.print_fake_bomb_board()
    game.print_neighbours_board()
    # print(game.cell_board)
    for i in range(10):
        col = int(input('open col: '))
        row = int(input('open row: '))

        game.open_cell(col, row)

        game.print_display()
