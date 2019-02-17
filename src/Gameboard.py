"""
Gameboard is responsible for managing the state of the game.  It is called by UI and in turn calls instances of Tiles.
"""

#This is the Gameboard class which will render the gameboard after a size and number of mines is initiated
import pygame
import random

# from src.Styles import Styles
from src.Tiles import Tiles

class Gameboard:
    """
    The Gameboard class maintains a 2-D list of Tiles objects in game_board, as well as various
    values that keep track of the game state.
    """

    # This was previously in the board_generator() function, but it needs to be
    # initialized outside of that function's scope for it to last the whole game

    # Constructor for initializing board values
    def __init__(self, board_size, mine_count, display):
        """
        Creates a new Gameboard object

        @pre: A board size and mine count are already determined by the user, and a Pygame display object is already created.
        @param board_size: The n dimension of the n x n board
        @param mine_count: The number of mines determined by user 
        @param display: the Pygame display object created by UI
        @post: A new Gameboard object is created
        @return: nothing
        """
        self.board_size = int(board_size)
        self.mine_count = int(mine_count)
        self.display    = display
        self.game_board = []
        self.total_mines = mine_count
        self.flag_count = self.mine_count #keeps a running total of number of flags used
        self.num_revealed_tiles = 0
        self.board_generator()
        

    # def loop(self): (TO BE FINISHED WHEN WE IMPLEMENT PYGAME)
        # while True:

    # Generate board and create tiles.
    def board_generator(self):
        """
        The gameboard is populated with tiles and randomly assigns mines to those tiles

        @pre: An empty Gameboard object exists
        @post: The Gameboard's game_board list is a 2D list filled with tiles
        @return: nothing
        """
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
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                self.count_adjacent_mines(x, y)

    def win(self):
        """
        win() is called along with lose() in every main gameplay loop, checking to see if the player has won

        @pre: win is called for every iteration of the main loop
        @post: Gameboard will decide whether or not to play the win screen  
        @return: True if the game is won, False otherwise
        """
        if (self.mine_count == self.total_mines):  #if number of correct used flags == total_mines
            return True  #win
        else:
            return False

    def lose(self, x, y):
        """
        Lose() is called along with win() in every main gameplay loop, as well as every time a Tiles object is clicked

        @pre: A tile is clicked or the win() condition is checked
        @param x: the x coordinate of the clicked tile
        @param y: the y coordinate of the clicked tile
        @post: Gameboard will decide whether or not to play the lose screen  
        @return: True if the game is lost, False otherwise
        """
        if (self.game_board[x][y].is_mine):
            return True  #lose
        else:
            return False        

    # Check and reveal surrounding tiles until base case or mine
    # It accepts coordinates as a position, checks if the coordinates are valid,
    # and calls other tiles recursively
    def rec_reveal(self, row, column):
        """
        This function recursively checks which tiles should be revealed, and adjusts the properties of each Tiles objects respectively

        @pre: A mine is clicked or rec_reveal() is called on by another Tiles object
        @param row: the row index of the revealed Tiles object
        @param column: the column index of the revealed Tiles object
        @post: The Tiles object is altered to be revealed or not, and its display is updated appropriately
        @return: nothing
        """
        if(((row >= 0 and row < self.board_size) and (column >= 0 and column < self.board_size)) and not self.game_board[row][column].is_mine and not self.game_board[row][column].is_revealed and not self.game_board[row][column].is_flag):
            self.game_board[row][column].tile_reveal()
            self.num_revealed_tiles += 1    #increment number of revealed tiles
            if (self.game_board[row][column].num_adjacent_mines == 0):
                # Update display (tile_reveal()) (TO BE FINISHED WHEN WE IMPLEMENT PYGAME)
                self.rec_reveal(row - 1, column)          # (UP)
                self.rec_reveal(row - 1, column - 1)
                self.rec_reveal(row + 1, column)          # (DOWN)
                self.rec_reveal(row + 1, column - 1)
                self.rec_reveal(row, column - 1)          # (LEFT)
                self.rec_reveal(row + 1, column + 1)
                self.rec_reveal(row, column + 1)          # (RIGHT)
                self.rec_reveal(row - 1, column + 1)


    def flag_reveal(self, row, column):
        """
        flag_reveal() is called when a flag is placed, checks the win condition and updates the Tiles object accordingly

        @pre: a flag is placed (right click)
        @param row: the row index of the placed flag
        @param column: the column index of the placed flag
        @post: the win condition is checked and the flag property of the Tiles object is updated
        """
        if self.game_board[row][column].is_mine == True and self.game_board[row][column].is_flag == True:
            return(self.game_board[row][column].tile_flag())
        elif self.game_board[row][column].is_mine == True and self.game_board[row][column].is_flag == False:
            return(self.game_board[row][column].tile_flag())
        else:
            return(self.game_board[row][column].tile_flag())

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
                # if self.game_board[x][y].is_mine:
                #     self.game_board[x][y].surf.fill((255,0,0))
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
        x_pos = int(board_position[0]) - 5
        y_pos = int(board_position[1]) - 5

        #divide by 35
        x_pos /= 35
        y_pos /= 35

        if ((not (self.win() and not (self.lose(int(x_pos), int(y_pos)))) and not (self.game_board[int(x_pos)][int(y_pos)].is_flag)):
            self.rec_reveal(int(x_pos), int(y_pos))
        elif (self.game_board[int(x_pos)][int(y_pos)].is_mine and not self.game_board[int(x_pos)][int(y_pos)].is_flag):
            self.lose(int(x_pos), int(y_pos))
            raise Exception('Oh no! You exploded!') #raise exception to be caught by the calling loop
        else:
            return 0

        if self.win():
            raise Exception('Congratulations, you win!') #raise exception to be caught by the calling loop

        if self.lose(int(x_pos), int(y_pos)):
            raise Exception('Oh no! You exploded!') #raise exception to be caught by the calling loop

    def call_flag(self):
            #get mouse position
            board_position = pygame.mouse.get_pos() #returns tuple of pixels

            #check if clicking on dead space
            for i in range(0, self.board_size+1):
                if (board_position[0] in range (35*i, 35*i+5)) or (board_position[1] in range (35*i, 35*i+5)):
                    return #do nothing

            #subtract 5 from board_position
            x_pos = int(board_position[0]) - 5
            y_pos = int(board_position[1]) - 5

            #divide by 35
            x_pos /= 35
            y_pos /= 35

            print(f"This is where a flag should be ({x_pos},{y_pos})")
            if(self.game_board[int(x_pos)][int(y_pos)].is_flag):
                self.flag_count += 1
                self.mine_count += self.flag_reveal(int(x_pos), int(y_pos))
            elif(self.flag_count == 0 and not (self.game_board[int(x_pos)][int(y_pos)].is_flag)):
                print(f"Current flag count is: {self.flag_count}")
                return 0
            else:
                self.mine_count += self.flag_reveal(int(x_pos), int(y_pos))
                self.flag_count -= 1
            print(f"Current flag count is: {self.flag_count}")

            if self.win(int(x_pos), int(y_pos)):
                raise Exception('Congratulations, you win!') #raise exception to be caught by the calling loop

            print(f"{self.mine_count}")
            print(f"{self.total_mines}")