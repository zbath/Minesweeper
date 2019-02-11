#This is the main executable of the program, it runs Game
import pygame
from pygame.locals import*

from src.UI import UI

pygame.init()

def main():

    board_size = input ("Enter board size (>=2): ")
    number_of_mines = input ("Enter number of mines: ")

    board_size = int(board_size)

    display = pygame.display.set_mode((5+board_size*35, 5+board_size*35))
    pygame.display.set_caption('Play Minesweeper!')

    user = UI(display)
    user.start_game(board_size, number_of_mines)

if __name__ == '__main__':
    main()