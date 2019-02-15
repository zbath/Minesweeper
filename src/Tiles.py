#This is the tile class go for the game
import pygame
from src.Styles import Styles
from random import randint
from src.Styles import Styles

class Tiles:

    flag_image = pygame.image.load("src/flag.png")
    num_adjacent_mines = 0
    pygame.font.init()
    mine_font = pygame.font.SysFont('Helvetica', 26)

    # Constructor initializing a Tile object
    # Tile object will be set to self, booleans(is_revealed, is_flag, is_mine)
    # Display will be called to draw a tile on the board
    def __init__(self, is_revealed, is_flag, is_mine, display): 
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
        #user_mines_found tracks how many tiles are CORRECTLY flagged
        users_mines_found = 0
        if self.is_flag == True:
            self.is_flag = False
        else:
            self.is_flag = True

            self.surf.blit(flag_image, (5, 5))
        if self.is_mine == True:
            #if tile clicked is mine, increment user_mines_found by 1
            users_mines_found = users_mines_found + 1