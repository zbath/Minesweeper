"""
Gameboard is responsible for managing the state of the game.  It is called by UI and in turn creates instances of Tiles.
"""
import pygame
import random
import copy
from src.Tiles import Tiles
from src.Animations_test import windisplay


flag_image = pygame.image.load("src/pixel_flag.png")
bomb_image = pygame.image.load("src/mine.jpg")


class Gameboard:
    """
    The Gameboard class maintains a 2-D list of Tiles objects in game_board, as well as various
    values that keep track of the game state.
    """
    def __init__(self, width, height, mine_count, display):
        """Sets initial values for member variables, generates new board stored in self.game_board.

        :param width: width of board
        :type width: int
        :param height: height of board
        :type height: int
        :param mine_count: number of mines
        :type mine_count: int
        :param display: pygame surface for drawing window
        :type display: pygame.Surface
        :return: None
        """
        self.winning=False
        self.cols = int(width)
        self.rows = int(height)
        self.mine_count = int(mine_count)
        self.game_board = []
        self.total_mines = mine_count
        self.flag_count = mine_count
        self.flagged_mines = 0
        self.num_revealed_tiles = 0
        self.number_of_tiles = 0
        self.trueMineCount = mine_count
        self.board_generator(display)

    def shuffle_tiles(self):
        """Shuffles tiles in self.game_board if not flagged or revealed, updates tile member variables.

        :return: None
        """

        # append all tiles to a 1-D list and shuffle
        tile_list = []
        for i in range(len(self.game_board)):
            for j in range(len(self.game_board[i])):
                tempTile = self.game_board[i][j]
                if not tempTile.is_revealed:
                    if not tempTile.is_flag:
                        tile_list.append(self.game_board[i][j])
                        self.game_board[i][j] = None
                
        random.shuffle(tile_list)

        # assign shuffled tile its new coordinates, update member vars, and append to new_board
        for i in range(len(self.game_board)):
            for j in range (len(self.game_board[i])):
                if not self.game_board[i][j]:
                    tempTile = tile_list[0]
                    tempTile.i = i
                    tempTile.j = j
                    tempTile.num_adjacent_mines = 0
                    tempTile.Rect = pygame.Rect((5 + 35 * tempTile.j), (5 + 35 * tempTile.i), 30, 30)
                    self.game_board[i][j] = tempTile
                    tile_list.pop(0)

        # recount mines
        for i in range(len(self.game_board)):
            for j in range(len(self.game_board[i])):
                self.count_adjacent_mines(i, j)

        self.winning=False

    def board_generator(self, display):
        """self.game_board is populated with Tiles objects and randomly assigns mines to those tiles.

        :param display: pygame surface for drawing window
        :type display: pygame.Surface
        :return: None
        """
        for i in range(self.rows):
            arr = []
            for j in range(self.cols):
                arr.append(Tiles(i, j, False, False, False, display))
            self.game_board.append(arr)

        # Randomly adds mines to the board until mine count equals zero
        while(self.mine_count > 0):
            random_row = random.randint(0, self.rows - 1)
            random_col = random.randint(0, self.cols - 1)

            if (not self.game_board[random_row][random_col].is_mine):
                self.game_board[random_row][random_col].is_mine = True
                self.mine_count -= 1

        # Counts number of adjacent mines at each tile
        for i in range(self.rows):
            for j in range(self.cols):
                self.count_adjacent_mines(i, j)

        #Count the number of tiles in the game
        for i in range(self.rows):
            for j in range(self.cols):
                self.number_of_tiles += 1

    def win(self):
        """Compare self.number_of_tiles and self.trueMineCount to num_revealed_tiles to determine if state is "win"

        :return: Bool, True if won else False
        """
        tilesToWin = self.number_of_tiles - self.trueMineCount
        if (int(self.num_revealed_tiles) == int(tilesToWin)):
            return True
        else:
            return False

    def winCondition(self):
        """*deprecated* Alternative method for raising win exception.

        :raise: Exception
        :return: None
        """
        raise Exception('Congratulations, you win!')

    def lose(self, i, j):
        """Return true if tile at coordinates is mine, else false

        :param i: row coordinate
        :param j: col coordinate
        :return: Bool, True if mine else False
        """
        if (self.game_board[i][j].is_mine):
            return True
        else:
            return False

    def rec_reveal(self, row, column):
        """Recursively call Tiles.tile_reveal on each tile and its surrounding

        :param row: row index
        :type row: int
        :param column: col index
        :type column: int
        :return: None
        """
        in_bounds = (row >= 0 and row < self.rows) and (column >= 0 and column < self.cols)
        not_mine = False
        not_revealed = False
        not_flagged = False

        if in_bounds:
            not_mine = not self.game_board[row][column].is_mine
            not_revealed = not self.game_board[row][column].is_revealed
            not_flagged = not self.game_board[row][column].is_flag

        if not_mine and not_revealed and not_flagged:
            self.game_board[row][column].tile_reveal()
            self.num_revealed_tiles += 1
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
        """Calls appropriate method to place flag depending on selected Tiles state.

        :param row: row index
        :type row: int
        :param column: column index
        :type column: int
        :return: int
        """
        if self.game_board[row][column].is_mine and self.game_board[row][column].is_flag:
            return(self.game_board[row][column].tile_flag())
        elif self.game_board[row][column].is_mine and not self.game_board[row][column].is_flag:
            return(self.game_board[row][column].tile_flag())
        else:
            return(self.game_board[row][column].tile_flag())

    def count_adjacent_mines(self, row, column):
        """Counts number of mines in adjacent tiles for display and assigns Tiles.num_adjacent_mines.

        :param row: row index
        :type row: int
        :param column: column index
        :type column: int
        :return: None
        """
        self.game_board[row][column].num_adjacent_mines = 0

	    #increment num_adjacent_mines including diagonals
        for row_inc in range (-1, 2):
            for col_inc in range (-1, 2):
			    #first check for valid indices
                increment_coord_in_bounds = (0 <= row+row_inc < self.rows) and ( 0 <= column + col_inc < self.cols)
                increment_not_zero = (not row_inc == 0) or (not col_inc == 0)
                if increment_coord_in_bounds and increment_not_zero:
                    #check if adjacent tile is a mine
                    if (self.game_board[row+row_inc][column+col_inc].is_mine):
                        self.game_board[row][column].num_adjacent_mines += 1

    def update_board(self, display, CheatModeEnabled=False):
        """This function creates and displays the board on the screen.

        :param display: surface to draw display on
        :type display: pygame.Surface
        :param CheatModeEnabled: turn on cheat mode?
        :type CheatModeEnabled: Bool
        :return: none
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
            self.DrawTile(self.game_board[i][j], display, CheatModeEnabled)

    def RevealAll(self, display):
        """Reveal all tiles at end of game.

        :param display: display surface to draw on
        :return: None
        """
        for i in range(self.rows):
            for j in range(self.cols):
                self.DrawTile(self.game_board[i][j], display, True)
        pygame.display.flip()

    def DrawTile(self, tile, display, CheatModeEnabled):
        """Draw tile according to its state.

        :param tile: Tiles object to draw
        :type tile: Tiles
        :param display: surface to draw on
        :type display: pygame.Surface
        :param CheatModeEnabled: is cheat mode enabled?
        :type CheatModeEnabled: bool
        :return: None
        """
        if tile.is_flag and not CheatModeEnabled:
            display.blit(flag_image, tile.Rect)
        elif tile.is_mine and CheatModeEnabled:
            display.blit(bomb_image, tile.Rect)
        elif tile.is_revealed:
            pygame.draw.rect(display, ((222,184,135)), tile.Rect)
            if tile.num_adjacent_mines > 0:
                color_plate=[(30, 144, 255), (0, 255, 0), (220, 20, 60)]
                adj_text = str(tile.num_adjacent_mines)
                font_surf = tile.mine_font.render(adj_text, True, color_plate[tile.randompick])
                display.blit(font_surf, tile.Rect)
                #pygame.display.update()
        else:
            pygame.draw.rect(display, (tile.org_color), tile.Rect)

    def detect_location(self):
        """After detecting click event, detect current location of mouse.

        :return: tuple
        """
        coords = pygame.mouse.get_pos()
        for i in range(len(self.game_board)):
            for j in range(len(self.game_board[i])):
                if(self.game_board[i][j].Rect.collidepoint(coords)):
                    return (i, j)

    def on_left_click(self, i, j, display):
        """Handle left-click on tile (rec_reveal, check if lose, check if win).

        :param i: row index
        :type i: int
        :param j: col index
        :type j: int
        :param display: surface to draw on
        :type display: pygame.Surface
        :raise: Exception
        :return: None
        """
        exploded = self.lose(i, j) and not self.game_board[i][j].is_flag

        self.rec_reveal(i, j)

        if exploded:
            raise Exception('Oh no! You exploded!')

        elif self.win():
            self.winning=True
            win= windisplay(self.cols, self.rows, display)
            win.displayfireworks()
            raise Exception('Congratulations, you win!')

    def on_right_click(self, i, j, display):
        """Handles right-click (flag_reveal, update flag count, checks for win).

        :param i: row index
        :type i: int
        :param j: col index
        :type j: int
        :param display: surface to draw on
        :type display: pygame.Surface
        :raise: Exception
        :return: None
        """
        in_bounds = i < self.rows and j < self.cols

        if in_bounds:
            if(self.game_board[i][j].is_flag):
                self.flag_count += 1
                self.mine_count += self.flag_reveal(i, j)
            else:
                self.mine_count += self.flag_reveal(i, j)
                self.flag_count -= 1

            if self.win():
                self.winning=True
                win= windisplay(self.cols, self.rows, display)
                win.displayfireworks()
                raise Exception('Congratulations, you win!') #raise exception to be caught by the calling loop

    def ToggleCheatMode(self, Enabled, display):
        """Display cheat-mode-altered board if Enabled, else re-draw regular board

        :param Enabled: is cheat mode selected?
        :type Enabled: bool
        :param display: surface to draw on
        :type display: pygame.Surface
        :return: None
        """
        if Enabled:
            # "reveal" all tiles and draw the board
            GameBoardCopy = copy.deepcopy(self)
            for i in range(GameBoardCopy.rows):
                for j in range(GameBoardCopy.cols):
                    GameBoardCopy.game_board[i][j].tile_reveal()
            GameBoardCopy.update_board(display, True)
        else:
            # redraw the covered board
            self.update_board(display)            
