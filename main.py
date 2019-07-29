"""
Basic pygame interface for minesweeper

- Written by SC 15/07/19
- edited by jmc 25/07/19
"""

import pygame
import numpy as np
from objects import Board

pygame.init()

# pygame interface variables
window_size = [510, 510]
font = pygame.font.Font('freesansbold.ttf', 30)
game = True

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

####### text example format, just keep it here to copy and paste
# text = font.render('testing', True, red)
# textRect = text.get_rect()
# textRect.center = (250, 250)

# create display
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

# board testing
testboard = [[0 for x in range(10)] for x in range(10)]
flag_board = [[False for x in range(10)] for x in range(10)]

# creating board and storing variables
board = Board()
bombs = board.bombs()
size = board.size()  # for now we just stick to 10

initialise = True


while game:

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
            game = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_press = pygame.mouse.get_pressed()
            left_click, middle_click, right_click = mouse_press[0], mouse_press[1], mouse_press[2]
            pos = pygame.mouse.get_pos()
            col = int(pos[0] // (cell_width + margin))
            row = int(pos[1] // (cell_height + margin))

            # condition for opening
            if initialise and left_click == 1:
                board.generate(row+1, col+1)  # created board object
                initialise = False

            # defining variables for easier access
            info_board = board.neighbours_board
            cell_board = board.cell_board

            cell = board.cell_board[row+1][col+1]

            # normal play starts here
            # click types and conditions
            if not initialise:
                if left_click == 1 and not cell.flagged():
                    board.open_cell(row+1, col+1)
                elif right_click == 1 and not cell.opened():
                    if cell.flagged():
                        cell.unflag()
                    else:
                        cell.flag()
                elif middle_click == 1:
                    pass  # do the reveal here
                print('Click {}. Grid coordinates {}, {}'.format(pos, row, col))

                for i in range(size):
                    for j in range(size):
                        cell = cell_board[i+1][j+1]
                        color = grey
                        if cell.flagged():
                            color = green
                        if cell.opened():
                            number = cell.value()
                            text = font.render(str(number), True, black)
                            textRect = text.get_rect()
                            textRect.center = (50 * i + 30, 50 * j + 30)

                            screen.blit(text, textRect)

                        pygame.draw.rect(screen, color, [(margin + cell_width) * j + margin,
                                                         (margin + cell_height) * i + margin,
                                                         cell_width, cell_height])

    clock.tick(60)

    pygame.display.flip()

# quitting game
pygame.quit()
quit()
