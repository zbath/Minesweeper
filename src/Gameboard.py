#This is the Gameboard class which will render the gameboard after a size and number of mines is initiated
import pygame

# from src.Styles import Styles
from Tiles import Tiles

class Gameboard:
    m_board = []
    m_size = 0
    m_mines = 0

    def make_tile(self, x_pos, y_pos):
        tile = Tile(x_pos, y_pos)
        return tile


    def __init__(self, size, mines):
        self.m_size = size
        self.m_mines = mines

        # Generating the 2d list of tiles (mines are not yet assigned):
        for i in range (0, self.m_size):
            x = []
            for j in range(0, self.m_size):
                x.append(self.make_tile(i, j))
            self.m_board.append(x)

