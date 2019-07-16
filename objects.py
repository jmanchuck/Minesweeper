import numpy as np


class Cell:
    def __init__(self, value=None, bomb=False, opened=False, flagged=False):
        """
        Args:
            _value (int): number of surrounding bombs (will be displayed)

            _bomb (bool): bomb or not

            _opened (bool): opened or not

            _flagged (bool): flagged or not
        """
        self._value = value
        self._bomb = bomb
        self._opened = opened
        self._flagged = flagged

    def open(self):  # when mouse click occurs to open, change cell state to opened
        self.opened = True

    def flag(self):  # when mouse click for flag, change cell state to flagged
        self.flagged = True

    def opened(self):
        return self._opened

    def value(self):
        return self._value

    def bomb(self):
        return self._bomb

    def flagged(self):
        return self._flagged


class Board:
    def __init__(self, size=8, bombs=16):
        
        """
        Parameters
            size (int): integer n for dimension n x n of square array (maybe change or extend to rectangle)

            bombs (int): number of bombs on the board (must be less than size^2)

        Attributes

            fake_bomb_board (2D np arr): array of booleans, True signifies a bomb. (n+2) x (n+2)

            bomb_board (2D np arr): same as above but without the extra 'False' surrounding it. n x n

            neighbours_board (2D np arr): array storing the information of adjacent bombs. n x n

            cell_board (2D list): list of Cell objects. Cell(value, bomb), default opened and flagged is False
        """
        
        self._size = size
        self._bombs = bombs
        self.fake_bomb_board = self.create_fake_bomb_board()
        self.bomb_board = self.create_bomb_board()
        self.neighbours_board = self.create_neighbours_board()
        self.cell_board = self.create_cell_board()

    def create_fake_bomb_board(self):
        """
        Returns:
             (n+2) x (n+2) 2D boolean array of bombs
        """

        # create an extra perimeter with no bombs around the board for ease of checking neighbours
        board_array = np.zeros((self.size+2, self.size+2), dtype=bool)

        num_bombs = 0

        while num_bombs < self.bombs:
            ind1 = np.random.randint(1,self.size+1)
            ind2 = np.random.randint(1,self.size+1)

            if board_array[ind1][ind2] != 1:
                board_array[ind1][ind2] = True
                num_bombs += 1

        return board_array

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
            return None # ignore this for bomb since we don't care

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

        # maybe could use this as main board since None values are bombs, anything else is an integer

        board = np.zeros((self.size, self.size))

        for i in range(self.size):
            for j in range(self.size):
                board[i][j] = self.return_neighbour(i+1, j+1)

        return board

    def print_neighbours_board(self):
        print(self.neighbours_board)

    def create_bomb_board(self):
        """
        Returns:
             n x n 2D boolean array of bombs
        """
        real_board = np.zeros((self.size, self.size), dtype=bool)

        for i in range(self.size):
            for j in range(self.size):
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

        cell_objects = [[None for x in range(self.size)] for x in range(self.size)]

        for i in range(self.size):
            for j in range(self.size):
                cell_objects[i][j] = Cell(neighbour_board[i][j], bombs_board[i][j])

        return cell_objects

    def size(self):
        return self._size

    def bombs(self):
        return self._bombs


class Actions:
    # this class can be implimented in the game loop
    def __init__(self):
        self._size = self.difficulty_select()
        self.bombs = self._size/3
        board = Board(self._size, self.bombs)

    @staticmethod
    def difficulty_select():
        # implement some kind of button later...
        difficulty = 5
        while difficulty not in range(0, 5):
            difficulty = input('Custom difficulty? 1 to 3, 3 is hardest')
        return difficulty*6

    def open_flag(self, row, col):
        return


game = Board()
game.print_bomb_board()
game.print_neighbours_board()
print(game.cell_board)
