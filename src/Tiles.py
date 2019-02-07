#This is the tile class go for the game
import pygame
from random import randint

class Tiles:
    def __init__(self, is_revealed, is_flag, is_mine): 
        self.is_revealed = is_revealed
        self.is_flag = is_flag
        self.is_mine = is_mine

    def tile_click():
        #calls tile_reveal, returns the state

    def tile_reveal():
        #if(is_mine):
            #return display
            #return boolean to board
            #is_revealed = true
        #if(is_flag):
            #return display
            #return boolean to board
            #is_revealed = false
        #if(not is_flag and not is_mine):
            #check if is_adjacent
            #recurse as needed
            #return display either numerical or blank
        

    def tile_flag():
        #call is_mine, if true, add total mine counter
        #return display
