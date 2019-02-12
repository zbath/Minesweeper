#This is the UI, it will handle the initial screen in which the User chooses the size of the board and number of mines
import pygame

from src.Gameboard import Gameboard

class UI:

    def __init__(self, display):
        self.display = display
        self.number_of_mines = 0
        self.board_size = 0

    def launch(self):
        
        clock = pygame.time.Clock() #adds clock imported from pygame

        #Get board size from user (still need to protect input)
        pre_game = True
        size_str = ""
        while pre_game:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pre_game = False
                        exit()
                    elif event.key != pygame.K_RETURN:
                        size_str += pygame.key.name(event.key)
                    else:
                        board_size = int(size_str)
                        pre_game = False
                elif event.type == pygame.QUIT:
                    exit()

            pygame.font.init()
            pre_game_font = pygame.font.SysFont('Helvetica', 40)
            
            temp_surf = pygame.display.set_mode((1000, 100))
            font_surf = pre_game_font.render('How big would you like your board (2 or larger)?  ' + size_str, True, (250, 250, 250))
            temp_surf.blit(font_surf, (5,25))
            
            pygame.display.flip()

        # Get number of mines from user (still need to protect input)
        pre_game = True
        mines_str = ""
        while pre_game:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pre_game = False
                        exit()
                    elif event.key != pygame.K_RETURN:
                        mines_str += pygame.key.name(event.key)
                    else:
                        number_of_mines = int(mines_str)
                        pre_game = False
                elif event.type == pygame.QUIT:
                    exit()

            pygame.font.init()
            pre_game_font = pygame.font.SysFont('Helvetica', 40)
            
            temp_surf = pygame.display.set_mode((1000, 100))
            font_surf = pre_game_font.render('How many mines do you want? It must be fewer than ' + str(board_size*board_size) + ": " + mines_str, True, (250, 250, 250))
            temp_surf.blit(font_surf, (5,25))
            
            pygame.display.flip()

        display = pygame.display.set_mode((5+board_size*35, 5+board_size*35))
        pygame.display.set_caption('Play Minesweeper!')
        user = UI(display)
        user.start_game(board_size, number_of_mines)

        self.start_game(board_size, number_of_mines)

        

    def start_game(self,board_size,number_of_mines):

        self.board_size = int(board_size)
        self.number_of_mines = int(number_of_mines)

        game_board = Gameboard(board_size, number_of_mines, self.display)

        clock = pygame.time.Clock() #adds clock imported from pygame

        running = True

        while running:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.QUIT:
                    exit()
        
            game_board.draw()
            pygame.display.flip()

        # pygame.display.update()
        clock.tick(30)

        # display = pygame.display.set_mode(
        #     (Styles['game']['width'],
        #     Styles['game']['width'])
        # )

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

    def left_click():
        # to be defined
        click = 0 #some dummy code to make code work

    def right_click():
        # to be defined
        click = 0 #some dummy code to make code work


