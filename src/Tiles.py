"""
The tiles class handles the states of each tile object, letting the program know if a certain tile is a flag, a mine, or already revealed.
"""
import pygame
import random
flag_image = pygame.image.load("src/pixel_flag.png")

class Tiles:

    num_adjacent_mines = 0
    pygame.font.init()
    mine_font = pygame.font.SysFont('Helvetica', 30)

    # Constructor initializing a Tile object
    # Tile object will be set to self, booleans(is_revealed, is_flag, is_mine)
    # Display will be called to draw a tile on the board
    def __init__(self, i, j, is_revealed, is_flag, is_mine, display):
        """
        @pre Initialization of a tile object
        @param
            is_revealed: takes a bool if tile object is already revealed
            is_flag: takes a bool if tile object is flagged
            is_mine: takes a bool if tile object is a mine
        @post Initializes display to display, surf to a surface size of 30x30 pixels, then fills each surface with a gray color"
        @return None
        """
        self.is_revealed = is_revealed
        self.i = i
        self.j = j
        self.is_flag = is_flag
        self.is_mine = is_mine
        #self.display = display
        self.Rect = pygame.Rect((5 + 35 * self.j), (5 + 35 * self.i), 30, 30)
        self.org_color=(50,205,50)
        self.isHoverbool = False
        self.hover_color = (152, 251, 152)
        self.randompick=random.randint(0, 2)

    def draw_self(self):
        """
        @pre Called from update_board in Gameboard.py
        @param
        @post Redraws the tile onto the board when doing an update to the gameboard, after a user action.
        @return
        """
        if self.is_flag:
            self.display.blit(flag_image, self.Rect)

        elif self.is_revealed:
            pygame.draw.rect(self.display, ((222,184,135)), self.Rect)
            if self.num_adjacent_mines > 0:
                color_plate=[(30, 144, 255), (0, 255, 0), (220, 20, 60)]
                adj_text = str(self.num_adjacent_mines)
                font_surf = self.mine_font.render(adj_text, True, color_plate[self.randompick])
                self.display.blit(font_surf, self.Rect)
                #pygame.display.update()
        else:
            pygame.draw.rect(self.display, (self.org_color), self.Rect)
            #pygame.display.update()

    def get_coords(self):
        """
        @pre Grabs the coordinate of a tile that has been specified in boardGame[i][j]
        @param
        @post
        @return Coordinates of the tile on the board
        """
        coords = (self.i, self.j)
        return coords

    # Draws number of adjacent mines to screen
    def tile_reveal(self):
        """
        Displays the number of mines surrounding a revealed tile (if any exist)

        @pre When user clicks and the specific tile(or area of recursively revealed tiles) it will change the tile to be revealed
        @param
        @post Shows the tile on the screen, changes tile objects value to true
        @return
        """
        self.is_revealed = True

    def tile_flag(self):
        """
        Adds or removes flag image on tile

        @pre Expects a call from a user right-click
        @param None
        @post Flag is displayed or removed from tile
        @return Returns an integer that will add or subtract from the flag count that is being compared to the mine count
        """
        if not self.is_revealed:
            if not self.is_flag:
                self.is_flag = True
                if self.is_mine:
                    return 1
                else:
                    return 0
            elif self.is_flag:
                self.is_flag = False
                if self.is_mine:
                    return -1
                else:
                    return 0
        else:
            return 0

    def refill(self):
        """
        @pre After tile is redrawn on the board it is filled
        @param

        @post
        @return
        """
        self.org_color=self.hover_color
        self.isHoverbool = True
    # Draws number of adjacent mines to screen
    def isHover(self):
        """
        @pre If user is looking at the tile
        @param
        @post Switch the values of the isHoverBool
        @return None
        """
        if not self.isHoverbool:
            return False
        else:
            return True

    def recoverColor(self):
        """
        @pre After refilling and redrawing, the color is back using this function
        @param
        @post When the color breaks from refilling, change the color back to the desired color
        @return None
        """
        self.org_color=(50,205,50)
        self.isHoverbool = False
