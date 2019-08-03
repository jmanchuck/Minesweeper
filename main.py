"""
Basic pygame interface for minesweeper

- Written by SC 15/07/19
- edited by jmc 25/07/19
"""

import pygame
from objects import Board

# creating board and storing variables
board = Board(12, 36)
bombs = board.bombs()
size = board.size()  # for now we just stick to 10

# generate pygame based on board
pygame.init()

# pygame text size
fontsize = 3*size
font = pygame.font.Font('freesansbold.ttf', fontsize)

# define colours
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
grey = (211, 211, 211)

# display properties
margin = size
cell_len = 4*size

width = size * (margin + cell_len) + margin
length = size * (margin + cell_len) + cell_len

window_size = [width, length]

# create display
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

initialise = True


def make_text(text, x, y, color):

    """
    Args:
        text (string/int): text to be displayed
        x (int), y(int): position
        color (var): one of the defined colors

    Blits the text passed into this function
    """

    text = font.render(str(text), True, color)
    textRect = text.get_rect()

    textRect.center = (x, y)
    screen.blit(text, textRect)


while board.play:

    # initial display
    if initialise:
        screen.fill(black)
        for row in range(size):
            for col in range(size):
                color = grey
                pygame.draw.rect(screen, color, [(margin + cell_len) * col + margin,
                                                 (margin + cell_len) * row + margin,
                                                 cell_len, cell_len])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            board.play = False
            pygame.quit()
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_press = pygame.mouse.get_pressed()
            left_click, middle_click, right_click = mouse_press[0], mouse_press[1], mouse_press[2]
            pos = pygame.mouse.get_pos()

            if pos[0] > (cell_len + margin) * size or pos[1] > (cell_len + margin) * size:
                continue

            col = 1 + int(pos[0] // (cell_len + margin))
            row = 1 + int(pos[1] // (cell_len + margin))

            # print('Click {}. Grid coordinates {}, {}'.format(pos, row, col))

            # condition for opening
            if initialise and left_click == 1:
                board.generate(row, col)  # created board object
                # make_text('Remaining: {}'.format(board.remaining), x/2, y - cell_len/2, white)
                initialise = False

            # defining variables for easier access
            info_board = board.neighbours_board
            cell_board = board.cell_board

            # define cell for clicked cell
            cell = cell_board[row][col]

            # normal play starts here
            if not initialise:

                # calling methods based on player choice
                if left_click == 1 and not cell.flagged() and not cell.opened():
                    board.open_cell(row, col)

                elif middle_click == 1 and not cell.flagged() and cell.opened():
                    board.open_neighbours(row, col)

                elif right_click == 1 and not cell.opened():
                    # print('flagging')
                    if cell.flagged():
                        cell.unflag()
                        board.remaining += 1
                    else:
                        cell.flag()
                        board.remaining -= 1

                # blit text for each cell
                for i in range(1, size + 1):
                    for j in range(1, size + 1):

                        # define new cell here, since we are looking at every single cell
                        cell = board.cell_board[i][j]
                        color = grey

                        # draw value if opened
                        if cell.opened():
                            # print("Index {}, {} is opened".format(i, j))
                            number = cell.value()

                            y = (cell_len + margin) * (i - 1) + cell_len/2 + margin
                            x = (cell_len + margin) * (j - 1) + cell_len/2 + margin

                            make_text(number, x, y, black)

                        # otherwise draw solid colour
                        else:
                            if cell.flagged():
                                color = green
                            pygame.draw.rect(screen, color, [(margin + cell_len) * (j - 1) + margin,
                                                             (margin + cell_len) * (i - 1) + margin,
                                                             cell_len, cell_len])

                # draw black strip over bottom text, then redraw remaining bombs text
                pygame.draw.rect(screen, black, (0, length - cell_len, width, cell_len))
                make_text('Remaining: {}'.format(board.remaining), width/2, length - cell_len/2, white)

    if not board.play:
        pygame.draw.rect(screen, black, (0, length - cell_len, width, cell_len))
        lose_text = '!!!!!!'

        make_text(lose_text, width / 2, length - cell_len / 2, red)

        pygame.display.flip()

        prompt = True

        while prompt:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    board.play = False
                    prompt = False

                # if right click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_press = pygame.mouse.get_pressed()
                    if mouse_press[2] == 1:
                        initialise = True
                        board.play = True
                        prompt = False

    clock.tick(60)

    pygame.display.flip()

# quitting game
pygame.quit()
quit()
