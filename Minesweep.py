"""
This is the main executable of the program, it runs UI.
"""
import pygame
from pygame.locals import*

import src.UI as UI

pygame.init()

def main():

    """
    @pre: none
    @post: initializes pygame and creates a UI object which runs the game
    """
    # TODO: initialize/create clock

    display = pygame.display.set_mode((1000, 100))
    pygame.display.set_caption('Play Minesweeper!')

    user = UI.UI(display) # TODO: pass clock to UI
    user.launch()

if __name__ == '__main__':
    main()