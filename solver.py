# algorithmic solver
# created 10/09/19 by jmc

from objects import Board, Cell


class Predict(Cell):
    """
    Inherits from cell object in objects.py
    Adds several attributes and methods to "predict" whether the cell is a bomb or not or what value it is
    """

    def __init__(self):
        super().__init__(None)
        self._prob = None


class Solver:

    """
    Gets the state of the board and solves
    """

    def __init__(self):
        self.board = None
        self.cell_board = None
        self.predict_board = None
        self._size = None

    def get_board(self, board):
        self.board = board
        self.cell_board = board.cell_board
        self._size = self.board.size()
        self.predict_board = [[Predict() for x in range(self._size)] for y in range(self._size)]

        for i in range(self._size):
            for j in range(self._size):
                self.predict_board[i][j].set_value(self.cell_board[i][j].value())
                if self.cell_board[i][j].opened():
                    self.predict_board[i][j].open()

    def print(self):
        for i in range(self._size):
            rows = []
            for j in range(self._size):
                if self.predict_board[i][j].opened():
                    rows.append("[{}]".format(self.predict_board[i][j].value()))
                else:
                    rows.append("[ ]")

            print("{} | {}".format(i, " ".join(rows)))


if __name__ == "__main__":
    game = Board()
    game.create_board(5, 5)
    solver = Solver()
    solver.get_board(game)
    solver.print()
