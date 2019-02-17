"""
This is the main executable of the program, it runs UI.
"""
import pygame
from pygame.locals import*

from src.UI import UI

pygame.init()

def main():

    """
    @pre: none
    @post: initializes pygame and creates a UI object which runs the game
    """

    display = pygame.display.set_mode((1000, 100))
    pygame.display.set_caption('Play Minesweeper!')

    user = UI(display)
    user.launch()

if __name__ == '__main__':
    main()