#This is the UI, it will handle the initial screen in which the User chooses the size of the board and number of mines
import pygame

from Gameboard import Board

class UI:

    def __init__(self, screen):
        self.screen = screen

    def start_game():

		#start screen

			#board_size = 1
			#number_of_mines = 0
        
		#Use a loop to obtain valid user input
		#while board_size < 2:
		#	print ("Enter board dimension (>= 2): ")
					#obtain user input for board_size

		#once a valid board size is obtain, get number of mines
		#while number_of_mines < 1:
			#        print ("Enter number of mines (>=1): ")
					#obtain user input for number_of_mines

			#Creates an instance of Gameboard -- call board_generator
                
			#Call run_game function -- we might have to make this a global variable so run_game can access the game board
			#run_game()

    def run_game():

			#game_victory = false
			#game_lost = false
        
			#Uses a loop to call is_not_mine (called when user clicks a tile)
			#while not game_victory or not game_lost:
					#obtain user input from clicking a tile (both right and left click)
                
					#call is_not_mine (a function in Gameboard that will call rec_reveal)
                
					#If all tiles are revealed (check every iteration), break the loop, user has won

					#If a mine is hit (is_not_mine returns false), break the loop, user has lost

					#Continues until a mine is hit or all tiles are revealed

    screen = pygame.screen.set_mode(
            (Styles['start_screen']['width'],
            Styles['start_screen']['width'])
        )

	def left_click();
	# to be defined
	def right_click();
	# to be defined


