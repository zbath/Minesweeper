#This is the tile class go for the game
import pygame
from src.Styles import Styles
from random import randint
from src.Styles import Styles
flag_image = pygame.image.load("src/pixel_flag.png")

class Tiles:
    """
    tile class creates the tiles on the gameboard and it's functionality per reveal
    """
    num_adjacent_mines = 0
    pygame.font.init()
    mine_font = pygame.font.SysFont('Helvetica', 26)

    # Constructor initializing a Tile object
    # Tile object will be set to self, booleans(is_revealed, is_flag, is_mine)
    # Display will be called to draw a tile on the board
    def __init__(self, is_revealed, is_flag, is_mine, display): 
        """
        initialize tile objects
        :param is_revealed:boolean of if tile is revealed
        :param is_flag: identifies if tile is flagged by user
        :param is_mine: boolean of tile being mine or not
        :param display: tile being seen on gameboard
        """
        self.is_revealed = is_revealed
        self.is_flag = is_flag
        self.is_mine = is_mine
        self.display = display
        self.surf = pygame.Surface((30,30))
        self.surf.fill((100,100,100))
  
    # Draws number of adjacent mines to screen
    def tile_reveal(self):
        self.is_revealed = True
        self.surf.fill((50,50,50))
        if(not self.is_flag and not self.is_mine):
            if self.num_adjacent_mines > 0:
                adj_text = str(self.num_adjacent_mines)
                font_surf = self.mine_font.render(adj_text, True, (250, 250, 250))
                self.surf.blit(font_surf, (5, 5))
        

    def tile_flag(self):
        if self.is_revealed == False:
            if self.is_flag == False:
                self.is_flag = True
                self.surf.blit(flag_image, (5, 5))
                if self.is_mine == True:
                    self.surf.blit(flag_image, (5, 5))
                    return(1)
                else: 
                    return 0
            elif self.is_flag == True:
                self.is_flag = False
                self.surf.fill((100, 100, 100))
                if self.is_mine == True:
                    self.surf.fill((100, 100, 100))
                    return(-1)
                else:
                    return 0
        else:
            return 0