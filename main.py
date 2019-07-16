"""
Basic pygame interface for minesweeper

- Written by SC 15/07/19
"""


import pygame

# pygame interface variables
display_width = 800
display_height = 600
game = True

# define colours
black = (0, 0, 0)
white = (255, 255, 255)

# create display
pygame.init()
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    gameDisplay.fill(white)
    pygame.display.update()
    clock.tick(60)

# quitting game
pygame.quit()
quit()
