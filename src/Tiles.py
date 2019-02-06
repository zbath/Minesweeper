import pygame

class Tile(object):
    # the _pos variables hold where on the board each tile lives
    # they start at 0
    x_pos = 0
    y_pos = 0

    # mine is True if the tile contains a mine, False otherwise
    # this will be determined at initilization
    is_mine = False
    is_revealed = False

    # num_mines contains how many mines are adjacent to this tile
    # this will have to be done after the ENTIRE board is generated
    num_mines = 0

    def __init__(self, x_pos, y_pos, is_mine):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.is_mine = is_mine

    def get_is_revealed(self):
        return (self.is_revealed)

    def get_is_mine(self):
        return(self.is_mine)

    def get_num_mines(self):
        return(self.num_mines)



