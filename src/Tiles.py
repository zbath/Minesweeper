#This is the tile class go for the game
import pygame
from src.Styles import Styles
from random import randint
from src.Styles import Styles

class Tiles:
    num_adjacent_mines = 0
    

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
  

    def tile_reveal(self):
        if(self.is_mine):
            return false #return a flag to Gameboard to end the game
            self.is_revealed = true
        if(not self.is_flag and not self.is_mine):
            if self.num_adjacent_mines > 0:
                #display number of adjacent
                self.display(self.num_adjacent_tiles)
            return true
        

    # def tile_flag(self):
    #     #user_mines_found tracks how many tiles are CORRECTLY flagged
    #     users_mines_found = 0
    #     Tile.is_flag = True
    #     if Tile.is_mine == True:
    #         #if tile clicked is mine, increment user_mines_found by 1
    #         users_mines_found = users_mines_found + 1
    #     #return display
    #     # ^included for now - do we need to display the flags from here?

        

