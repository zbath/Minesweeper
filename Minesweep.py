import pygame

from src.Game import Game

def main():
    display = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption('Play Minesweeper!')

    game = Game(display)
    game.loop()

if __name__ == '__main__':
    main()