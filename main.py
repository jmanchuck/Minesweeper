"""
Basic pygame interface for minesweeper

- Written by SC 15/07/19
- edited by jmc 25/07/19
"""

import pygame
from objects import Board

pygame.init()

# pygame interface variables
window_size = [510, 540]
font = pygame.font.Font('freesansbold.ttf', 30)

# define colours
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
grey = (211, 211, 211)

# display properties
margin = 10
cell_width = 40
cell_height = 40

# create display
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

# creating board and storing variables
board = Board()
bombs = board.bombs()
size = board.size()  # for now we just stick to 10

initialise = True
game = True


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
        for row in range(10):
            for col in range(10):
                color = grey
                pygame.draw.rect(screen, color, [(margin + cell_width) * col + margin,
                                                 (margin + cell_height) * row + margin,
                                                 cell_width, cell_height])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            board.play = False
            pygame.quit()
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_press = pygame.mouse.get_pressed()
            left_click, middle_click, right_click = mouse_press[0], mouse_press[1], mouse_press[2]
            pos = pygame.mouse.get_pos()

            if pos[0] > (cell_width + margin) * size or pos[1] > (cell_height + margin) * size:
                continue

            col = 1 + int(pos[0] // (cell_width + margin))
            row = 1 + int(pos[1] // (cell_height + margin))

            print('Click {}. Grid coordinates {}, {}'.format(pos, row, col))

            # condition for opening
            if initialise and left_click == 1:
                board.generate(row, col)  # created board object
                make_text('Remaining: ', 200, 525, white)
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
                    print('flagging')
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

                            y = 50 * (i - 1) + 30
                            x = 50 * (j - 1) + 30

                            make_text(number, x, y, black)

                        # otherwise draw solid colour
                        else:
                            if cell.flagged():
                                color = green
                            pygame.draw.rect(screen, color, [(margin + cell_width) * (j - 1) + margin,
                                                             (margin + cell_height) * (i - 1) + margin,
                                                             cell_width, cell_height])


                # draw the number of remaining bombs, first clearing then re draw
                pygame.draw.rect(screen, black, (345, 510, 50, 30))
                make_text(board.remaining, 360, 525, white)

    if not board.play:
        lose_text = 'You lose! Right click to play again'

        make_text(lose_text, 255, 270, red)

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
