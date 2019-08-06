"""
Basic pygame interface for minesweeper

- Written by SC 15/07/19
- edited by jmc 25/07/19
"""

import pygame
from objects import Board

# initialise board size and number of bombs
board = Board(10, 25)
bombs = board.bombs()
size = board.size()  # for now we just stick to 10

pygame.init()

# pygame text size
fontsize = 3*size
font = pygame.font.Font('freesansbold.ttf', fontsize)

# define colours
green = (0, 135, 56)
blue = (0, 0, 255)
red = (128, 13, 0)
turquoise = 12, 179, 151
black = (0, 0, 0)
white = (255, 255, 255)
grey = (140, 140, 140)
lightgrey = (207, 207, 207)

# for printing numbers in different colours
colourlist = [blue, green, red, red, turquoise, black, grey]

# loading images
flag = pygame.image.load('images/flag.png')
flag = pygame.transform.scale(flag, (fontsize, fontsize))
bomb = pygame.image.load('images/bomb.png')
bomb = pygame.transform.scale(bomb, (fontsize, fontsize))

# window and display dimensions
margin = int(size/2)
cell_len = 4*size

width = size * (margin + cell_len) + margin
length = size * (margin + cell_len) + cell_len
window_size = [width, length]

# create display
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

initialise = True
win = False


def make_text(text, x, y, color):
    """ Blits text centred around position x, y """

    text = font.render(str(text), True, color)
    textRect = text.get_rect()

    textRect.center = (x, y)
    screen.blit(text, textRect)


def make_image(x, y, img):
    """ Blits image centred around position x, y """

    img_rect = img.get_rect()
    img_rect.center = (x, y)
    screen.blit(img, img_rect)


while board.play:

    # initial display
    if initialise:
        screen.fill(black)
        for row in range(size):
            for col in range(size):
                pygame.draw.rect(screen, lightgrey, [(margin + cell_len) * col + margin,
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
                board.print_neighbours_board()

                # defining variables for easier access
                info_board = board.neighbours_board
                cell_board = board.cell_board

            # normal play starts here
            if not initialise:

                # define cell for clicked cell
                cell = cell_board[row][col]

                # calling methods based on player choice
                if left_click == 1 and not cell.flagged():
                    if not cell.opened():
                        board.open_cell(row, col)
                    else:
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
                all_opened = 0
                for i in range(1, size + 1):
                    for j in range(1, size + 1):

                        # define new cell here, since we are looking at every single cell
                        cell = board.cell_board[i][j]
                        color = lightgrey
                        y = (cell_len + margin) * (i - 1) + cell_len / 2 + margin
                        x = (cell_len + margin) * (j - 1) + cell_len / 2 + margin

                        # draw value if opened
                        if cell.opened():
                            # print("Index {}, {} is opened".format(i, j))
                            number = cell.value()
                            if number == -1:
                                make_image(x, y, bomb)
                            else:
                                make_text(number, x, y, colourlist[number - 1])
                                all_opened += 1

                        # otherwise draw solid colour
                        else:
                            pygame.draw.rect(screen, color, [(margin + cell_len) * (j - 1) + margin,
                                                             (margin + cell_len) * (i - 1) + margin,
                                                             cell_len, cell_len])
                            if cell.flagged():
                                make_image(x, y, flag)

                # draw black strip over bottom text, then redraw remaining bombs text
                pygame.draw.rect(screen, black, (0, length - cell_len, width, cell_len))
                make_text('Remaining: {}'.format(board.remaining), width/2, length - cell_len/2, white)

    if board.remaining == 0 and all_opened == size**2 - bombs:
        board.play = False
        win = True

    if not board.play:

        if win:
            text = 'All mines found!'
        else:
            text = '!!!!!!'

        pygame.draw.rect(screen, black, (0, length - cell_len, width, cell_len))
        make_text(text, width / 2, length - cell_len / 2, red)

        pygame.display.flip()

        prompt = True

        while prompt:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    board.play = False
                    prompt = False

                # if right click, replay
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
