#This is the Gameboard class which will render the gameboard after a size and number of mines is initiated
import pygame
import random

# from src.Styles import Styles
from src.Tiles import Tiles

class Gameboard:

    # This was previously in the board_generator() function, but it needs to be
    # initialized outside of that function's scope for it to last the whole game

    # Constructor for initializing board values
    def __init__(self, board_size, mine_count, display):
        self.board_size = int(board_size)
        self.mine_count = int(mine_count)
        self.display    = display
        self.game_board = []
        self.total_mines = mine_count
        self.board_generator()
        

    # def loop(self): (TO BE FINISHED WHEN WE IMPLEMENT PYGAME)
        # while True:

    # Generate board and create tiles.
    def board_generator(self):
        # Traverse game board and fill with tiles.
        for x in range(0, self.board_size):
            arr = []
            for y in range(0, self.board_size):
                arr.append(Tiles(False, False, False, self.display))
            self.game_board.append(arr)

        # Randomly adds mines to the board until mine count equals zero
        # Creates two random numbers in range of board size and checks arr[][] at that location
        # Adds a mine to that location if one does not already exist
        while(self.mine_count > 0):
            random_row = random.randint(0, self.board_size - 1)
            random_col = random.randint(0, self.board_size - 1)
            
            if (not self.game_board[random_row][random_col].is_mine):
                self.game_board[random_row][random_col].is_mine = True
                self.mine_count -= 1

        # Counts number of adjacent mines at each tile
        # A nested for loop calling count_adjacent_mines() at each tile
        # count_adjacent_mines() will send count to Tiles object
        for x in range(0, self.board_size - 1):
            for y in range(0, self.board_size - 1):
                self.count_adjacent_mines(x, y)
        

    # Check and reveal surrounding tiles until base case or mine
    # It accepts coordinates as a position, checks if the coordinates are valid,
    # and calls other tiles recursively
    def rec_reveal(self, row, column):
        if(((row >= 0 and row < self.board_size) and (column >= 0 and column < self.board_size)) and not self.game_board[row][column].is_mine and not self.game_board[row][column].is_revealed):
            self.game_board[row][column].is_revealed = True
            if (self.game_board[row][column].num_adjacent_mines == 0):
                # Update display (tile_reveal()) (TO BE FINISHED WHEN WE IMPLEMENT PYGAME)
                self.game_board[row][column].tile_reveal()
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
                if (((row+row_inc < self.board_size) and (column + col_inc < self.board_size) and ((not row_inc == 0) or (not col_inc == 0))) and row+row_inc >= 0 and column+col_inc >= 0):
                    #check if adjacent tile is a mine
                    if (self.game_board[row+row_inc][column+col_inc].is_mine):
                        self.game_board[row][column].num_adjacent_mines+=1

    def draw(self):
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                if self.game_board[x][y].is_mine:
                    self.game_board[x][y].surf.fill((255,0,0))
                self.display.blit(self.game_board[x][y].surf, ((5+35*x),(5+35*y)))
        pygame.display.flip()

    def detect_location(self):
        #get mouse position
        board_position = pygame.mouse.get_pos() #returns tuple of pixels

		#check if clicking on dead space
        for i in range(0, self.board_size+1):
            if (board_position[0] in range (35*i, 35*i+5)) or (board_position[1] in range (35*i, 35*i+5)):
                return #do nothing

        #subtract 5 from board_position
        board_position[0] = board_position[0] - 5
        board_position[1] = board_position[1] - 5

        #divide by 35
        board_position /= 5
        row = board_position[0]
        col = board_position[1]
        self.game_board[row][col].rec_reveal()
