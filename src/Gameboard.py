#This is the Gameboard class which will render the gameboard after a size and number of mines is initiated
import pygame

# from src.Styles import Styles
from Tiles import Tile

class Gameboard:

    # Constructor for initializing board values
    def __init__(self, board_size, mine_count, display):
        self.board_size = board_size
        self.mine_count = mine_count
        self.display    = display

    # def loop(self): (TO BE FINISHED WHEN WE IMPLEMENT PYGAME)
        # while True:

    # Generate board and create tiles.
    def board_generator():
        game_board = [[None],[None]] # Creates an empty game board, 2D list
        while(mine_count > 0):# while loop for mine_count > 0
            random_row = random.randint(0, self.board_size) # chooses a random row number
            random_col = random.randint(0, self.board_size) # chooses a random column number
            if (game_board[random_row][random_column] not Tile.check_is_mine()):
                game_board[random_row][random_column] = Tile(False, False, True)
                mine_count -= 1
        for row_index, row in enumerate(game_board): #for loop iterating through rows
             for col_index, value in enumerate(game_board): #for loop iterating through cols
                if not Tile.check_is_mine():
                    game_board[row_index][column_index] = Tile(False, False, False)

    # Check and reveal surrounding tiles until base case or mine
    def rec_reveal(row, column):
        if(((row > 0 and row < board_size) and (column > 0 and column < board_size)) and not check_is_mine)
            # Update display (tile_reveal()) (TO BE FINISHED WHEN WE IMPLEMENT PYGAME)
            rec_reveal(arr[row-1][column])          # (UP)
            rec_reveal(arr[row+1][column])          # (DOWN)
            rec_reveal(arr[row][column-1])          # (LEFT)
            rec_reveal(arr[row][column+1])          # (RIGHT)

