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
  

# #    def tile_reveal():
#         #if(is_mine):
#             #return display
#             #return boolean to board
#             #is_revealed = true
#         #if(not is_flag and not is_mine):
#         #if num_adjacent_mines > 0 -> display numerical value
#         #else display blank
        

#     def tile_flag(self):
#         count = 0
#         #call is_mine, if true, add total mine counter
#         #return display
#         if self.is_mine == True:
#             count = count + 1

