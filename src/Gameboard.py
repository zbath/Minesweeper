"""
Gameboard is responsible for managing the state of the game.  It is called by UI and in turn calls instances of Tiles.
"""

#This is the Gameboard class which will render the gameboard after a size and number of mines is initiated
import pygame
import random

from src.Tiles import Tiles
from src.Animations_test import windisplay

class Gameboard:
    """
    The Gameboard class maintains a 2-D list of Tiles objects in game_board, as well as various
    values that keep track of the game state.
    """

    # This was previously in the board_generator() function, but it needs to be
    # initialized outside of that function's scope for it to last the whole game

    # Constructor for initializing board values
    def __init__(self, width, height, mine_count, display):
        """
        Creates a new Gameboard object

        @pre: A board size and mine count are already determined by the user, and a Pygame display object is already created.
        @param board_size: The n dimension of the n x n board
        @param mine_count: The number of mines determined by user
        @param display: the Pygame display object created by UI
        @post: A new Gameboard object is created
        @return: nothing
        """
        self.winning=False
        self.cols = int(width)
        self.rows = int(height)
        self.mine_count = int(mine_count)
        self.display    = display
        self.game_board = []
        self.total_mines = mine_count
        self.flag_count = mine_count #keeps a running total of number of flags used
        self.num_revealed_tiles = 0
        self.winning=False
        self.board_generator()


    # Generate board and create tiles.
    def board_generator(self):
        """
        The gameboard is populated with tiles and randomly assigns mines to those tiles

        @pre: An empty Gameboard object exists
        @post: The Gameboard's game_board list is a 2D list filled with tiles
        @return: nothing
        """
        # Traverse game board and fill with tiles.
        for i in range(self.rows):
            arr = []
            for j in range(self.cols):
                arr.append(Tiles(i, j, False, False, False, self.display))
            self.game_board.append(arr)

        # Randomly adds mines to the board until mine count equals zero
        # Creates two random numbers in range of board size and checks arr[][] at that location
        # Adds a mine to that location if one does not already exist
        while(self.mine_count > 0):
            random_row = random.randint(0, self.rows - 1)
            random_col = random.randint(0, self.cols - 1)

            if (not self.game_board[random_row][random_col].is_mine):
                self.game_board[random_row][random_col].is_mine = True
                self.mine_count -= 1

        # Counts number of adjacent mines at each tile
        # A nested for loop calling count_adjacent_mines() at each tile
        # count_adjacent_mines() will send count to Tiles object
        for i in range(self.rows):
            for j in range(self.cols):
                self.count_adjacent_mines(i, j)

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

    def lose(self, i, j):
        """
        Lose() is called along with win() in every main gameplay loop, as well as every time a Tiles object is clicked

        @pre: A tile is clicked or the win() condition is checked
        @param x: the x coordinate of the clicked tile
        @param y: the y coordinate of the clicked tile
        @post: Gameboard will decide whether or not to play the lose screen
        @return: True if the game is lost, False otherwise
        """
        if (self.game_board[i][j].is_mine):
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
        in_bounds = (row >= 0 and row < self.rows) and (column >= 0 and column < self.cols)

        if in_bounds:
            not_mine = not self.game_board[row][column].is_mine
            not_revealed = not self.game_board[row][column].is_revealed
            not_flagged = not self.game_board[row][column].is_flag

        if in_bounds and not_mine and not_revealed and not_flagged:
            self.game_board[row][column].tile_reveal()
            self.num_revealed_tiles += 1    #increment number of revealed tiles
            if (self.game_board[row][column].num_adjacent_mines == 0):
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
        if self.game_board[row][column].is_mine and self.game_board[row][column].is_flag:
            return(self.game_board[row][column].tile_flag())
        elif self.game_board[row][column].is_mine and not self.game_board[row][column].is_flag:
            return(self.game_board[row][column].tile_flag())
        else:
            return(self.game_board[row][column].tile_flag())

    # Counts number of mines adjacent to a given tile
    # It accepts position through row and column parameters
	# According to these coordinates, it determines whether an adjacent tile is valid
	# and if it is a mine. If it is a mine, increments num_adjacent_mines
    def count_adjacent_mines(self, row, column):

        """
        This function counts the number of mines adjacent to a given tile.

        @pre: Gameboard has already been created and mines have been randomly assigned to tiles.
        @post: Updates each tile with the number of mines adjacent to it.
        @param row: the current row of the gameboard
        @param col: the current col of the gameboard
        """

	#increment num_adjacent_mines including diagonals
        for row_inc in range (-1, 2):
            for col_inc in range (-1, 2):
			    #first check for valid indices
                increment_coord_in_bounds = (0 <= row+row_inc < self.rows) and ( 0 <= column + col_inc < self.cols)
                increment_not_zero = (not row_inc == 0) or (not col_inc == 0)  # TODO: Change range(-1, 2) to tuple
                if increment_coord_in_bounds and increment_not_zero:
                    #check if adjacent tile is a mine
                    if (self.game_board[row+row_inc][column+col_inc].is_mine):
                        self.game_board[row][column].num_adjacent_mines+=1

    def update_board(self):
        """
        This function creates and displays the board on the screen.

        @pre: user has inputted board_size and mine count.
        @post: Draws the board and displays on screen.
        """
        if not self.winning:
            x_pos=0
            y_pos=0
            Pass=False
            coords = pygame.mouse.get_pos()
            for i in range(len(self.game_board)):
             for j in range(len(self.game_board[i])):
               if(self.game_board[i][j].Rect.collidepoint(coords)):
                    Pass=True
                    x_pos=i
                    y_pos=j

            if not self.game_board[x_pos][y_pos].is_revealed and not self.game_board[x_pos][y_pos].is_flag and Pass:
                  self.game_board[x_pos][y_pos].refill()

        for i in range(self.rows):
         for j in range(self.cols):
            if not self.winning and self.game_board[i][j].isHover() and (i != x_pos or j != y_pos):
                if self.game_board[i][j].is_flag:
                        pass
                else:
                   self.game_board[i][j].recoverColor()
            self.game_board[i][j].draw_self()
        #pygame.display.update()

    def detect_location(self):
        coords = pygame.mouse.get_pos()
        for i in range(len(self.game_board)):
            for j in range(len(self.game_board[i])):
                if(self.game_board[i][j].Rect.collidepoint(coords)):
                    print(f'Detected: ({self.game_board[i][j].i}, {self.game_board[i][j].j}{", mine!" if self.game_board[i][j].is_mine else ""})')
                    return (i, j)
                    #TODO: rewrite backend logic to use [i][j] values

    def on_left_click(self, i, j):
        exploded = self.lose(i, j) and not self.game_board[i][j].is_flag
        valid_tile = not (self.game_board[i][j].is_flag or self.game_board[i][j].is_revealed)
        end_state = self.win() or exploded

        if not end_state and not self.game_board[i][j].is_flag:
            self.rec_reveal(i, j)

        elif exploded:
            raise Exception('Oh no! You exploded!')  # raise exception to be caught by the calling loop

        elif self.win():
            self.winning=True
            win= windisplay(self.cols, self.rows, self.display)
            win.displayfireworks()
            raise Exception('Congratulations, you win!')  # raise exception to be caught by the calling loop



    # def detect_location(self):
    #     """
    #     This function detects click location and calculates where the click occurs with respect to the gameboard.
    #
    #     @pre: User has clicked the screen.
    #     @post: Determines where the user has clicked with respect to the gameboard and determines winning/losing conditions.
    #     @exception: throws an exception when the game should end (win/lose)
    #     """
    #     #get mouse position
    #     board_position = pygame.mouse.get_pos() #returns tuple of pixels
    #
		# #check if clicking on dead space
    #     for i in range(0, self.rows+1):
    #         if board_position[1] in range (35*i, 35*i+5):
    #             print ("Bad click (y-dir)")
    #             return #do nothing
    #
    #     for i in range(0, self.cols+1):
    #         if board_position[0] in range (35*i, 35*i+5):
    #             print ("Bad click (x-dir)")
    #             return #do nothing
    #
    #     #subtract 5 from board_position
    #     y_pos = int(board_position[0]) - 5
    #     x_pos = int(board_position[1]) - 5
    #
    #     #divide by 35
    #     x_pos //= 35
    #     y_pos //= 35
    #
    #     if x_pos < self.cols and y_pos < self.rows:
    #         if ((not (self.win() and not (self.lose(int(x_pos), int(y_pos)))) and not (self.game_board[int(x_pos)][int(y_pos)].is_flag))):
    #             self.rec_reveal(int(x_pos), int(y_pos))
    #         elif (self.game_board[int(x_pos)][int(y_pos)].is_mine and not self.game_board[int(x_pos)][int(y_pos)].is_flag):
    #             self.lose(int(x_pos), int(y_pos))
    #             raise Exception('Oh no! You exploded!') #raise exception to be caught by the calling loop
    #         else:
    #             return 0
    #
    #         if self.win():
    #             raise Exception('Congratulations, you win!') #raise exception to be caught by the calling loop
    #
    #         if self.lose(int(x_pos), int(y_pos)):
    #             raise Exception('Oh no! You exploded!') #raise exception to be caught by the calling loop


    def on_right_click(self, i, j):
        """
        This function manages flagging behavior.

        @pre: The user has "right-clicked" and method is called from UI.
        @post: Detects location of mouse with respect to the gameboard and manages flagging behavior. Also determines if the game has been won or lost.
        @exception: throws an exception when the game should end (win/lose)
        """
        in_bounds = i < self.rows and j < self.cols

        if in_bounds:
            if(self.game_board[i][j].is_flag):
                self.flag_count += 1
                self.mine_count += self.flag_reveal(i, j)
            elif(self.flag_count == 0 and not (self.game_board[i][j].is_flag)):
                return 0
            else:
                self.mine_count += self.flag_reveal(i, j)
                self.flag_count -= 1

            if self.win():
                self.winning=True
                win= windisplay(self.cols, self.rows, self.display)
                win.displayfireworks()
                raise Exception('Congratulations, you win!') #raise exception to be caught by the calling loop
