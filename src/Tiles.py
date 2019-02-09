#This is the tile class go for the game
import pygame
from random import randint
from src.Styles import Styles

class Tiles:
    # Constructor initializing a Tile object
    # Tile object will be set to self, booleans(is_revealed, is_flag, is_mine)
    # Tile object will have an x_pos and y_pos initialized
    # Display will be called to draw a tile on the board
    def __init__(self, is_revealed, is_flag, is_mine, x_pos, y_pos, is_adjacent, num_adjacent_mines, display): 
        self.is_revealed = is_revealed
        self.is_flag = is_flag
        self.is_mine = is_mine
        self.is_adjacent = is_adjacent
        self.num_adjacent_mines = num_adjacent_mines
        self.display = display
        self.num_adjacent_mines = 0
        #self.x_pos = Styles[x][y]
        #self.y_pos = Styles[x][y]

    # Given x_pos and y_pos, a tile will call styles to be drawn and displayed
    # at the coordinate point, scaled to size
    def draw(self, x_pos, y_pos):
        pygame.draw.rect(
            self.display,
            Styles['color']['white'],
            [
                self.x_pos,
                self.y_pos,
            ]
        )

    def tile_click():
        #calls tile_reveal, returns the state
		if not is_revealed:
			#call tile_reveal
			tile_reveal()

		#return state
		return self


#    def tile_reveal():
        #if(is_mine):
            #return display
            #return boolean to board
            #is_revealed = true
        #if(not is_flag and not is_mine):
        #if num_adjacent_mines > 0 -> display numerical value
        #else display blank
        
    # When called, boolean is_flag will be set to true
    # Displays a flag on the tile
    # If is_mine is true, adds to the count
    def tile_flag():
        count = 0
        #call is_mine, if true, add total mine counter
        #return display
        if is_mine == True:
            count = count + 1

        i = index[0]
        j = index[1]
        button_key = str(i) + "," + str(j)
        button_val = self.view.buttons[button_key]       
        if button_val["bg"] == "grey":
            button_val.configure(bg="yellow", text="FLAG")
            self.cells_flagged.append(button_key)
        elif button_val["text"] == "FLAG":
            button_val.configure(bg="grey", text="")
            self.cells_flagged.remove(button_key)
        self.update_mines()
        
        #pygame.mouse.get_pressed() - can return tuple (leftclick,middleclick,rightclick)
        #features to add:
        #physical response to button click from user (right mouse button click) (click = pygame.mouse.get_pressed())
        #keep track of the validity of user picking mine or not
        #if it is last one and all mines marked, game is won. Winning handled in "gambeboard", but include boolean
        #otherwise, just add to counter if it IS a mine
        #every click displays flag

    # Sets is_mine to true for the Tile object
    def set_mine():
        is_mine = True

    # Returns the truth value of is_mine
    def get_mine():
        return is_mine

    def tile_click():
        #calls tile_reveal, returns the state
		if not is_revealed:
			#call tile_reveal
			tile_reveal()

		#return state
		return self