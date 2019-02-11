#This is the main executable of the program, it runs Game
import pygame
from pygame.locals import*

from src.UI import UI

pygame.init()

def main():
    display = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption('Play Minesweeper!')

    user = UI(display)
    user.start_game()

if __name__ == '__main__':
    main()