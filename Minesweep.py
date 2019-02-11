#This is the main executable of the program, it runs Game
import pygame
from pygame.locals import*

from src.UI import UI

pygame.init()

def main():

    board_size = input ("Enter board size (>=2): ")
    number_of_mines = input ("Enter number of mines: ")

    display = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption('Play Minesweeper!')

    user = UI(display)
    user.start_game(board_size, number_of_mines)

if __name__ == '__main__':
    main()