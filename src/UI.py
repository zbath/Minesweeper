#This is the UI, it will handle the initial screen in which the User chooses the size of the board and number of mines
import pygame

from src.Gameboard import Gameboard

class UI:

    def __init__(self, display):
        self.display = display

    def start_game(self):

        board_size = 1
        number_of_mines = 0

        clock = pygame.time.Clock() #adds clock imported from pygame

		#freezes when user input is requested
        #board_width = input ("Enter board size (>=2): ")
        #number_of_mines = input ("Enter number of mines: ")

        running = True

        while running: #sets the main game loop
            #create a surface
            surf = pygame.Surface((300,300))
			#sets color of board
            surf.fill((0, 0, 255))
            rect = surf.get_rect()
			
			#draws the surface at these coordinates
            self.display.blit(surf, (400, 300))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.QUIT:
                    exit()
        Gameboard.draw()

        pygame.display.update()
        clock.tick(30)

        display = pygame.display.set_mode(
            (Styles['game']['width'],
            Styles['game']['width'])
        )

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
					#obtain user input from clicking a tile
                
					#call is_not_mine (a function in Gameboard that will call rec_reveal)
                
					#If all tiles are revealed (check every iteration), break the loop, user has won

					#If a mine is hit (is_not_mine returns false), break the loop, user has lost

					#Continues until a mine is hit or all tiles are revealed

        screen = pygame.screen.set_mode(
            (Styles['start_screen']['width'],
            Styles['start_screen']['width'])
        )

    def left_click():
        # to be defined
        click = 0 #some dummy code to make code work

    def right_click():
        # to be defined
        click = 0 #some dummy code to make code work


