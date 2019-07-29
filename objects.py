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
        self.bomb_board = None
        self.neighbours_board = None
        self.cell_board = None
        self.display = [['_' for x in range(self._size+2)] for x in range(self._size+2)]

    def create_bomb_board(self, init_row, init_col):
        """
        Args:
            init_col (int): initial col selection
            init_row (int): initial row selection, ensures there is no bomb on first selection
        Returns:
             (n+2) x (n+2) 2D boolean array of bombs
        """

        # create an extra perimeter with no bombs around the board for ease of checking neighbours
        board_array = np.zeros((self._size + 2, self._size + 2), dtype=bool)

        num_bombs = 0

        while num_bombs < self._bombs:
            ind1 = np.random.randint(1, self._size + 1)
            ind2 = np.random.randint(1, self._size + 1)

            if ind1 in [init_row - 1, init_row, init_row + 1] and ind2 in [init_col - 1, init_col, init_col + 1]:
                continue

            elif not board_array[ind1][ind2]:
                board_array[ind1][ind2] = True
                num_bombs += 1

        return board_array

    def print_bomb_board(self):
        print(self.bomb_board)

    def return_neighbour(self, row, col):
        """
        Args:
            col (int): column index
            row (int): row index
        Returns:
            number of bombs in immediate neighbour (max 8) for a specific position
            None if position is bomb
        """
        if self.bomb_board[row][col]:  # bomb is -1
            return -1

        else:
            neighbours = 0

            for i in [row-1, row, row+1]:
                for j in [col-1, col, col+1]:
                    if self.bomb_board[i][j]:
                        neighbours += 1
            return neighbours

    @staticmethod
    def neighbour_coord(row, col):
        """
        Args:
            row (int), col(int)
        Returns:
            List of all neighbours in the form of a tuple (i,j)
        """
        neighbour_list = []
        for i in [row - 1, row, row + 1]:
            for j in [col - 1, col, col + 1]:
                neighbour_list.append((i, j))

        neighbour_list.remove((row, col))

        return neighbour_list

    def create_neighbours_board(self):  # can print this board to see all information
        """
        Returns
            2D array storing how many neighbours are bombs for each cell, bomb cells are -1
        """
        board = np.zeros((self._size + 2, self._size + 2)).astype(int)

        for i in range(1, self._size+1):  # indexes from 1 to size
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

        cell_objects = [[None for x in range(self._size + 2)] for x in range(self._size + 2)]

        for i in range(0, self._size + 2):
            for j in range(0, self._size + 2):
                cell_objects[i][j] = Cell(neighbour_board[i][j], bomb_board[i][j])

        return cell_objects

    def generate(self, init_row, init_col):
        """
        Creates board attributes, opens initial board
        Args:
            init_row (int): initial row that is opened
            init_col (int): initial column that is opened
        """
        if init_col > self._size or init_row > self._size:
            print('index out of range, game size is {}'.format(self._size))
            print('rerun and don\'t troll please')
            quit()

        self.bomb_board = self.create_bomb_board(init_row, init_col)
        self.neighbours_board = self.create_neighbours_board()
        self.cell_board = self.create_cell_board()
        self.open_cell(init_row, init_col)

    def open_cell(self, row, col):
        """
        Args:
            col (int)
            row (int)

        Handles opening cells using the Cell object, with flooding condition
        """
        cell = self.cell_board[row][col]
        if not cell.opened():
            cell.open()

            if cell.value() == 0:
                for (surr_row, surr_col) in self.neighbour_coord(row, col):
                    if 0 < surr_row <= self._size and 0 < surr_col <= self._size:
                        self.open_cell(surr_row, surr_col)

    def open_neighbours(self, row, col):
        adj_flags = 0
        for (surr_row, surr_col) in self.neighbour_coord(row, col):
            if self.cell_board[surr_row][surr_col].flagged():
                adj_flags += 1
        if adj_flags == cell.value():
            for (surr_row, surr_col) in self.neighbour_coord(row, col):
                self.open_cell(surr_row, surr_col)

    def update_display(self):
        for row in range(self._size+2):
            for col in range(self._size+2):
                cell = self.cell_board[row][col]
                if cell.opened():
                    if cell.bomb():
                        self.display[row][col] = '!'
                    else:
                        self.display[row][col] = str(self.neighbours_board[row][col])
                elif cell.flagged():
                    self.display[row][col] = 'X'

                elif not cell.flagged():
                    self.display[row][col] = '_'

    def print_display(self):
        real_display = [[None for x in range(self._size)] for x in range(self._size)]

        for i in range(self._size):
            for j in range(self._size):
                real_display[i][j] = self.display[i+1][j+1]
        print('\n', '##### DISPLAY #####')
        for r in real_display:
            print(" ".join(r))

    def size(self):
        return self._size

    def bombs(self):
        return self._bombs


if __name__ == "__main__":
    play = True
    print('Default game size is 8x8 with 16 bombs')
    game = Board()  # put in args to change size and no. of bombs, i.e. Board(12, 36) for 12x12 and 36 bombs

    bombs = game.bombs()
    size = game.size()
    remaining = bombs

    print('Top left is 1,1. First index represents row, second index represents column')
    print('Initial open')
    # column and row starts from 1 from top left to bottom right
    game.generate(int(input('Open row: ')), int(input('Open col: ')))
    # game.print_neighbours_board() # print this for answers
    game.update_display()
    game.print_display()

    print('indexing starts from 1 when opening cells')

    while play:
        badInput = True
        while badInput:
            try:
                choice = input('open (o) or flag (f) followed by row and column, e.g. o,3,3: ').split(',')
                row = int(choice[1])
                col = int(choice[2])
            except IndexError:
                print('Invalid input')
                continue
            if row not in range(1, size+1) and col not in range(1, size+1):
                print('Invalid input')
                continue
            cell = game.cell_board[row][col]
            if choice[0].lower() == 'o':
                game.open_cell(row, col)
                if game.cell_board[row][col].bomb():
                    print('is a bomb you die')
                    play = False
                badInput = False

            elif choice[0].lower() == 'f':
                if cell.opened():
                    print('Invalid, cell is opened')
                elif cell.flagged():
                    cell.unflag()
                    remaining += 1
                    badInput = False
                else:
                    cell.flag()
                    remaining -= 1
                    badInput = False

        if remaining == 0:
            play = False

        game.update_display()
        game.print_display()
        print('remaining bombs: {}'.format(remaining))
        print('__' * size)
