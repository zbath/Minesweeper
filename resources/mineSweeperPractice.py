
	# @author Taylor Bauer and whoever else wants to work on it
	# @date Feb 5, 2019
	# @file mineSweeperPractice.py
	# @brief Very rough framework in which to implement Minesweeper game logic

# Things this implementation DOES NOT HAVE:
#     -A win state
#     -A mine position assignment function worth a dang
#     -pygame implementation
#     -Any sort of recursive logic that reveals others squares than the one currently being revealed
#     -Any logic that counts adjacent mines


# random is only used for my temporary and janky way of assigning mine positions
import random

class Tile(object):
    # the Pos variables hold where on the board each tile lives
    # they start at 0
    xPos = 0
    yPos = 0
    mine = False
    revealed = False
    adjacent = 0

    def __init__(self, xPos, yPos, mine):
        self.xPos = xPos
        self.ypos = yPos
        self.mine = mine
    

# x- and y-position are set at initilization
# as well as whather or not the tile is hiding a mine
def make_tile(xPos, yPos, mine):
    tile = Tile(xPos, yPos, mine)
    return tile




# For my purposes the board is always a 5x5, but its generation is actually coded to
# be more flexible. The tiles are held in a 2D list called arr.
class Board:
    tileWidth = 5
    tileHeight = 5
    mineCount = 1
    running = True
    arr = []

def count_adjacent_mines(board, row, column):
    for row_inc in range (-1, 2):
        for col_inc in range (-1, 2):
            if (((row+row_inc < board.tileHeight) and (column + col_inc < board.tileWidth) and ((not row_inc == 0) or (not col_inc == 0))) and row+row_inc >= 0 and column+col_inc >= 0):
                if (board.arr[row+row_inc][column+col_inc].mine):
                    board.arr[row][column].adjacent+=1

def rec_reveal(board, row, column):
    if(((row >= 0 and row < board.tileHeight) and (column >= 0 and column < board.tileWidth)) and not board.arr[row][column].mine and not board.arr[row][column].revealed):
        board.arr[row][column].revealed = True
        if (board.arr[row][column].adjacent == 0):
            rec_reveal(board, row - 1, column)          # (UP)
            rec_reveal(board, row + 1, column)          # (DOWN)
            rec_reveal(board, row, column - 1)          # (LEFT)
            rec_reveal(board, row, column + 1)          # (RIGHT)        

# At startup, generate a Board object called game
game = Board()
# below is us populating the 2d list of tiles
for i in range (0, game.tileHeight):
    x = []
    for j in range(0, game.tileWidth):
        mineDecider = random.choice((False, False, False, False, False, True)) 
        # ^I know this is janky, I still need to learn how to do it better
        x.append(make_tile(i, j, mineDecider))
    game.arr.append(x)

for i in range (0, game.tileHeight):
    for j in range (0, game.tileWidth):
        if (not game.arr[i][j].mine):
            count_adjacent_mines(game, i, j)


# This is just for showing the user where the mines are after generation
for i in range (0, game.tileHeight):
    for j in range (0, game.tileWidth):
        if (game.arr[i][j].mine):
            print ('X', end='')
        else:
            print (game.arr[i][j].adjacent, end='')
        if (j == (game.tileWidth - 1)):
            print ('')


# The main game loop:
while (game.running == True):

    print("\n\n\n\n")
    print("Here is your current board: \n")

    # For now, the board displays an X for every unrevealed tile and
    # a blank space for each revealed tile
    for i in range (0, game.tileHeight):
        for j in range (0, game.tileWidth):
            if (game.arr[i][j].revealed):
                print (game.arr[i][j].adjacent, end='')
            else:
                print ('X', end='')
            if (j == (game.tileWidth - 1)):
                print ('')

    # The guesses need to be between 0 and (size - 1)
    # There's no protection around these, so be careful
    yGuess = input("\nWhere would you like to click (x-position)? ")
    xGuess = input("Where would you like to click (y-position)? ")

    # There's a losing state implemented, but no winning state yet
    if (game.arr[int(xGuess)][int(yGuess)].mine):
        print ("There was a mine there! You Lose!\n")
        game.running = False

    else:
        rec_reveal(game, int(xGuess), int(yGuess))

    game.arr[int(xGuess)][int(yGuess)].revealed = True
    





