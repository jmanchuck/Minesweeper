import numpy as np


class Cell:
    def __init__(self, value=None, bomb=False, opened=False, flagged=False):
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
        self._size = size
        self._bombs = bombs
        self.pseudo_board = self.create_array()
        self.neighbours_board = self.create_neighbours_board()
        self.final_board = self.object_board()

    def create_array(self):
        board_array = np.zeros((self._size+2, self._size+2), dtype=bool)
        num_bombs = 0

        while num_bombs < self._bombs:
            ind1 = np.random.randint(1, self._size+1)
            ind2 = np.random.randint(1, self._size+1)
            if board_array[ind1][ind2] != 1:
                board_array[ind1][ind2] = True
                num_bombs += 1

        return board_array

    def print_board(self):
        print(self.pseudo_board)

    def cell_create(self):
        # not sure what the point of this is -SC
        cells = [self._size]
        pass

    def return_neighbour(self, col, row):
        if self.pseudo_board[col][row]:  # it doesn't really matter for a bomb...
            return None
        else:
            neighbours = 0
            for i in [col-1, col, col+1]:
                for j in [row-1, row, row+1]:
                    if i == col and j == row:
                        pass
                    else:
                        # print('checking for ', i, j)
                        if self.pseudo_board[i][j]:
                            neighbours += 1
            return neighbours

    def create_neighbours_board(self):
        board = np.zeros((self._size, self._size))
        for i in range(self._size):
            for j in range(self._size):
                board[i][j] = self.return_neighbour(i+1, j+1)
        return board

    def print_neighbours_board(self):
        print(self.neighbours_board)

    def bombs_board(self):
        new_arr = np.zeros((self._size, self._size), dtype=bool)
        for i in range(self._size):
            for j in range(self._size):
                new_arr[i][j] = self.pseudo_board[i+1][j+1]
        return new_arr

    def object_board(self):
        bombs_board = self.bombs_board()
        neighbour_board = self.neighbours_board
        cell_objects = [[None for x in range(self._size)] for x in range(self._size)]
        for i in range(self._size):
            for j in range(self._size):
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


game = Board(3, 5)
game.print_board()
game.print_neighbours_board()
game.object_board()
