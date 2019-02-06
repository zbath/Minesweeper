import pygame

class Tile(object):
    # the _pos variables hold where on the board each tile lives
    # they start at 0
    m_x_pos = 0
    m_y_pos = 0

    # mine is True if the tile contains a mine, False otherwise
    # this will be determined at initilization
    m_is_mine = False
    m_is_revealed = False

    # num_mines contains how many mines are adjacent to this tile
    # this will have to be done after the ENTIRE board is generated
    m_num_mines = 0

    def __init__(self, x_pos, y_pos):
        self.m_x_pos = x_pos
        self.m_y_pos = y_pos

    def get_is_revealed(self):
        return (self.m_is_revealed)

    def get_is_mine(self):
        return(self.m_is_mine)

    def get_num_mines(self):
        return(self.m_num_mines)

    # accepts num_mines after it is calculated by Gameboard
    def set_num_mines(self, num_mines):
        self.m_num_mines = num_mines
        return (0)
    

        
