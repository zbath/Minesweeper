#This is the UI, it will handle the initial screen in which the User chooses the size of the board and number of mines
import pygame

from src.Gameboard import Gameboard
instructions_image = pygame.image.load("src/user_instructions.png")

class UI:
    """
    create user interface 
    """

    def __init__(self, display):
        """
        initialize UI
        :param display: display of board
        """
        self.display = display
        self.number_of_mines = 0
        self.board_size = 0

    # This is a pre-game function.  It obtains information
    # from the user about what size the board should be and
    # how many mines they would like and passes it on to
    # start_game() which then generates the board
    def launch(self):
        """
        create board initialization
        User input of size of board and number of mines
        """
        
        clock = pygame.time.Clock() #adds clock imported from pygame

        #instruction screen
        pygame.font.init()
        instructions_font = pygame.font.SysFont('Helvetica', 40)
        temp_surf = pygame.display.set_mode((1200, 400))
        temp_surf.blit(instructions_image, (5,30))
        pygame.display.flip()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.QUIT:
                    exit()
            pygame.display.flip()

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
                        if pygame.key.name(event.key).isdigit():
                            size_str += pygame.key.name(event.key)
                        elif event.key == pygame.K_BACKSPACE:
                            size_str = size_str[:-1]
                    else:
                        if size_str != "":
                            self.board_size = int(size_str)
                            if (self.board_size < 2) or (self.board_size > 40):
                                self.board_size = 0
                                size_str = ""
                            else:
                                pre_game = False
                elif event.type == pygame.QUIT:
                    exit()
            
            

            pygame.font.init()
            pre_game_font = pygame.font.SysFont('Helvetica', 40)
            
            if (self.board_size < 2):
                temp_surf = pygame.display.set_mode((1200, 100))
                font_surf = pre_game_font.render('How big would you like your board (1 < n < 39)?  ' + size_str, True, (250, 250, 250))
                temp_surf.blit(font_surf, (5,30))
            
            pygame.display.flip()
            clock.tick()

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
                        if pygame.key.name(event.key).isdigit():
                            mines_str += pygame.key.name(event.key)
                        elif event.key == pygame.K_BACKSPACE:
                            mines_str = mines_str[:-1]
                    else:
                        if mines_str != "":
                            number_of_mines = int(mines_str)
                            if (number_of_mines >= self.board_size*self.board_size) or (number_of_mines == 0):
                                number_of_mines = 0
                                mines_str = ""
                            else:
                                pre_game = False
                elif event.type == pygame.QUIT:
                    exit()

            temp_surf = pygame.display.set_mode((1200, 100))
            font_surf = pre_game_font.render('How many mines would you like? (It must be fewer than ' + str(self.board_size*self.board_size) + "): " + mines_str, True, (250, 250, 250))
            temp_surf.blit(font_surf, (5,30))
            
            pygame.display.flip()
            clock.tick()

#######################################################
        #instruction screen
#        pygame.font.init()
#        instructions_font = pygame.font.SysFont('Helvetica', 40)
#        temp_surf = pygame.display.set_mode((1200, 400))
#        temp_surf.blit(instructions_image, (5,30))
#        pygame.display.flip()

#        running = True

#        while running:
#            for event in pygame.event.get():
#                if event.type == pygame.KEYDOWN:
#                    if event.key == pygame.K_ESCAPE:
#                        running = False
#                elif event.type == pygame.QUIT:
#                    exit()
##########################################################

        display = pygame.display.set_mode((5+self.board_size*35, 5+self.board_size*35))
        pygame.display.set_caption('Play Minesweeper!')
        user = UI(display)
        user.start_game(self.board_size, number_of_mines)      

    def start_game(self,board_size,number_of_mines):
        """
        begin game by pygame clock and interact with key pressed by user
        """

        self.board_size = int(board_size)
        self.number_of_mines = int(number_of_mines)

        game_board = Gameboard(board_size, number_of_mines, self.display)

        clock = pygame.time.Clock() #adds clock imported from pygame

        running = True

        word = ' '

        while running:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.QUIT:
                    exit()
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    position = pygame.mouse.get_pos()
                    try:
                        game_board.detect_location()
                    except Exception as statement:
                        word = str(statement)
                        running = False
                        break
                elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3):
                    position = pygame.mouse.get_pos()
                    game_board.call_flag()
                    #Tile.tile_flag(position[0], position[1])
                
        
            game_board.draw()
            pygame.display.flip()

        #end game screen
        pygame.font.init()
        end_game_font = pygame.font.SysFont('Helvetica', 40)
        temp_surf = pygame.display.set_mode((1200, 100))
        font_surf = end_game_font.render(word, True, (250, 250, 250))
        temp_surf.blit(font_surf, (5,30))
        pygame.display.flip()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.QUIT:
                    exit()
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    position = pygame.mouse.get_pos()
                        
                elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3):
                    position = pygame.mouse.get_pos()
                    #Tile.tile_flag(position[0], position[1])

