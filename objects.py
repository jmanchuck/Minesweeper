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
    def __init__(self, size=6, bombs=6):
        """
        Args:
            size (int): integer n for dimension n x n of square array (maybe change or extend to rectangle)

            bombs (int): number of bombs on the board (must be less than size^2)

        Attributes:
            bomb_board (2D np arr): array of booleans, True signifies a bomb. (n+2) x (n+2)

            neighbours_board (2D np arr): array storing the information of adjacent bombs. (n+2) x (n+2)

            cell_board (2D list): list of Cell objects. Cell(value, bomb), default opened and flagged is False (n+2) x (n+2)

            display_board (2D np arr): n x n display board
        """
        self._size = size
        self._bombs = bombs
        self.bomb_board = None
        self.neighbours_board = None
        self.cell_board = None
        self.display_board = [['_' for x in range(self._size)] for x in range(self._size)]

    def create_bomb_board(self, init_col, init_row):
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

            if ind1 in [init_row-1, init_row, init_row+1] and ind2 in [init_col-1, init_col, init_col+1]:
                continue

            elif not board_array[ind1][ind2]:
                board_array[ind1][ind2] = True
                num_bombs += 1

        return board_array

    def print_bomb_board(self):
        print(self.bomb_board)

    def return_neighbour(self, col, row):
        """
        Args:
            col (int): column index
            row (int): row index
        Returns:
            number of bombs in immediate neighbour (max 8) for a specific position
            None if position is bomb
        """
        if self.bomb_board[col][row]:  # bomb is -1
            return -1

        else:
            neighbours = 0

            for i in [col-1, col, col+1]:
                for j in [row-1, row, row+1]:
                    if i == col and j == row:
                        pass
                    else:
                        if self.bomb_board[i][j]:
                            neighbours += 1

            return neighbours

    def create_neighbours_board(self):  # can print this board to see all information
        """
        Returns
            2D array storing how many neighbours are bombs for each cell, bomb cells are -1
        """

        board = np.zeros((self._size+2, self._size+2)).astype(int)

        for i in range(1, self._size+1):
            for j in range(1, self._size+1):
                board[i][j] = self.return_neighbour(i, j)

        return board

    def print_neighbours_board(self):
        print(self.neighbours_board)

    def create_cell_board(self):
        """
        Returns:
            2D list of Cell objects
        """
        bomb_board = self.bomb_board

        neighbour_board = self.neighbours_board

        cell_objects = [[None for x in range(self._size+2)] for x in range(self._size+2)]

        for i in range(0, self._size+2):
            for j in range(0, self._size+2):
                cell_objects[i][j] = Cell(neighbour_board[i][j], bomb_board[i][j])

        return cell_objects

    def print_display(self):
        print('##### DISPLAY #####')
        for row in self.display_board:
            print(" ".join(row))
        print('___________________')

    def open_cell(self, col, row):
        """
        Args:
            col (int)
            row (int)

        Handles opening cells using the Cell object.

        let me know if any index errors come up -jj
        """
        self.cell_board[col][row].open()
        if self.cell_board[col][row].bomb():
            self.display_board[col-1][row-1] = '!'
        else:
            try:
                self.display_board[col-1][row-1] = str(self.cell_board[col][row].value())
            except IndexError:
                print('you tried to index {}, {}'.format(col, row))
            print('cell {}, {} has been opened'.format(col, row))

    def flag_cell(self, col, row):
        self.cell_board[col][row].flag()

        self.display_board[col][row] = 'X'

    def size(self):
        return self._size

    def bombs(self):
        return self._bombs

    def create(self, init_col, init_row):
        """
        Creates board attributes, calls adj_zero to generate first open
        Args:
            init_col (int): initial column that is opened
            init_row (int): initial row that is opened
        """

        if init_col > self._size or init_row > self._size:
            print('index out of range, game size is {}'.format(self._size))
            print('game exiting...')
            quit()

        self.bomb_board = self.create_bomb_board(init_col, init_row)
        self.neighbours_board = self.create_neighbours_board()
        self.cell_board = self.create_cell_board()

        zero = [(init_col, init_row)]

        while len(zero) > 0:
            new_ind = []
            for indices in zero:
                ind1 = indices[0]
                ind2 = indices[1]
                for j in self.adj_zeros(ind1, ind2):
                    new_ind.append(j)
            zero = list(set(new_ind))

    def adj_zeros(self, col, row):
        """
        Opens non-zero neighbours and opens current cell
        Args:
            col (int): column
            row (int): row

        Returns:
            Indices of unopened adjacent 0s (no bombs next to them)
        """

        blank_unopened = []
        if 0 < col < self._size+1 and 0 < row < self._size+1:
            self.open_cell(col, row)
            for i in [col-1, col, col+1]:
                for j in [row-1, row, row+1]:
                    if not self.cell_board[i][j].opened():
                        if self.neighbours_board[i][j] == 0:
                            blank_unopened.append((i, j))
                        else:
                            try:
                                self.open_cell(i, j)
                            except IndexError:
                                print('you tried to index {}, {}'.format(i, j))

        return blank_unopened

    def open_neighbours(self, col, row):
        """
        Args:
             col (int)
             row (int)
        """
        for i in [col-1, col, col+1]:
            for j in [row-1, row, row+1]:
                self.open_cell(i, j)


if __name__ == "__main__":
    game = Board()

    print('Default game size is 6x6, change this in class Board init')

    # column and row starts from 1 from top left to bottom right
    game.create(int(input('open col: ')), int(input('open row: ')))

    game.print_neighbours_board()
    game.print_display()

    print('indexing starts from 1 when opening cells')

    for i in range(10):
        col = int(input('open col: '))
        row = int(input('open row: '))

        game.open_cell(col, row)

        game.print_display()
