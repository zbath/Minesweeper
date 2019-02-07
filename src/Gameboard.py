#This is the Gameboard class which will render the gameboard after a size and number of mines is initiated
import pygame
import random

# from src.Styles import Styles
from Tiles import Tile

class Gameboard:


    # This was previously in the board_generator() function, but it needs to be
    # initialized outside of that function's scope for it to last the whole game
    game_board = [[None],[None]] # Creates an empty game board, 2D list
    mine_count = 0
    board_size = 0

    # Constructor for initializing board values
    def __init__(self, board_size, mine_count, display):
        self.board_size = board_size
        self.mine_count = mine_count
        self.display    = display


    # def loop(self): (TO BE FINISHED WHEN WE IMPLEMENT PYGAME)
        # while True:

    # Generate board and create tiles.
    def board_generator(self):
        game_board = [[None],[None]] # Creates an empty game board, 2D list
        while(self.mine_count > 0):# while loop for mine_count > 0
            random_row = random.randint(0, self.board_size) # chooses a random row number
            random_col = random.randint(0, self.board_size) # chooses a random column number

            # Will this work if the actual list of tiles isn't implemented yet?
            # Don't we need to use .append() to add things to lists?
            if (not game_board[random_row][random_col].is_mine()):
                game_board[random_row][random_col] = Tile(False, False, True)
                self.mine_count -= 1
        for row_index, row in enumerate(game_board): #for loop iterating through rows
             for col_index, value in enumerate(game_board): #for loop iterating through cols
                if not game_board[row_index][col_index].is_mine():  
                    game_board[row_index][col_index] = Tile(False, False, False)

    # Check and reveal surrounding tiles until base case or mine
    # It accepts coordinates as a position, checks if the coordinates are valid,
    # and calls other tiles recursively 
    def rec_reveal(self, row, column):
        if(((row >= 0 and row < self.board_size) and (column >= 0 and column < self.board_size)) and not self.game_board[row][column].is_mine()):
            # Update display (tile_reveal()) (TO BE FINISHED WHEN WE IMPLEMENT PYGAME)
            self.rec_reveal(row - 1, column)          # (UP)
            self.rec_reveal(row + 1, column)          # (DOWN)
            self.rec_reveal(row, column - 1)          # (LEFT)
            self.rec_reveal(row, column + 1)          # (RIGHT)

    # Counts number of mines adjacent to a given tile
    # It accepts position through row and column parameters
	# According to these coordinates, it determines whether an adjacent tile is valid
	# and if it is a mine. If it is a mine, increments num_adjacent_mines
    def count_adjacent_mines(self, row, column):
	#increment num_adjacent_mines including diagonals
        for row_inc in range (-1, 2):
            for col_inc in range (-1, 2):
			    #first check for valid indices
                if (self.board_size <= (row+row_inc) or self.board_size <= (column+col_inc)):
                    #check if adjacent tile is a mine
                    if (self.game_board[row+row_inc][column+col_inc].is_mine()):
                        self.game_board[row][column].num_adjacent_mines+=1
