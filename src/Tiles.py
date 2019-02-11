#This is the tile class go for the game
import pygame
from src.Styles import Styles
from random import randint

class Tiles:
    def __init__(self, is_revealed, is_flag, is_mine, display): 
        self.is_revealed = is_revealed
        self.is_flag = is_flag
        self.is_mine = is_mine
        self.display = display
        self.num_adjacent_mines = 0
        self.surf = pygame.Surface((30,30))
        self.surf.fill((100,100,100))

        #self.x_pos = Styles[x][y]
        #self.y_pos = Styles[x][y]

    # def draw(self, x_pos, y_pos):
    #     pygame.draw.rect(
    #         self.display,
    #         Styles['color']['white'],
    #         [
    #             self.x_pos,
    #             self.y_pos,
    #         ]
    #     )

    # def tile_click(self):
    #     #calls tile_reveal, returns the state
    #     if not is_revealed:
    #         #call tile_reveal
    #         tile_reveal()

        #return state


#    def tile_reveal():
        #if(is_mine):
            #return display
            #return boolean to board
            #is_revealed = true
        #if(not is_flag and not is_mine):
            #check if is_adjacent
            #recurse as needed
            #return display either numerical or blank
        

    def tile_flag(self):
        count = 0
        #call is_mine, if true, add total mine counter
        #return display
        if self.is_mine == True:
            count = count + 1

               
        #pygame.mouse.get_pressed() - can return tuple (leftclick,middleclick,rightclick)
        #features to add:
        #physical response to button click from user (right mouse button click) (click = pygame.mouse.get_pressed())
        #keep track of the validity of user picking mine or not
        #if it is last one and all mines marked, game is won. Winning handled in "gambeboard", but include boolean
        #otherwise, just add to counter if it IS a mine
        #every click displays flag
