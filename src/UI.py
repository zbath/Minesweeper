"""
Class UI handles the ins and outs of the User Interface including but not limited to the start of the program window, user input, and game loop.

    pydoc -w UI
"""

#This is the UI, it will handle the initial screen in which the User chooses the size of the board and number of mines
import pygame
from src.Gameboard import Gameboard
instructions_image = pygame.image.load("src/user_instructions.png")

class UI:
    """
    UI initializes a display for the user to interact with the program.
    """
    def __init__(self, display):
        """
        Constructs a new 'UI' object.

        @pre Initialized at start of program called from executive 'Minesweep.py'
        @param
            display: Takes a display mode from executive 'Minesweep.py'
        @post Initializes display to the param passed in
        @return None
        """
        #self.click_sound=click_sound
        self.display = display
        self.number_of_mines = 0
        self.board_size = 0

    # This is a pre-game function.  It obtains information
    # from the user about what size the board should be and
    # how many mines they would like and passes it on to
    # start_game() which then generates the board
    def launch(self):
        """
        Initializes the launch of the game, receives input from user and passes input to 'start_game()'.

        @pre Expects a UI to be initialized
        @param
            self: One entire self of UI object
        @post Starts game based on user input of board size and number of mines
        @return None
        """


        #instruction screen
        pygame.font.init()
        instructions_font = pygame.font.SysFont('Helvetica', 40)
        temp_surf = pygame.display.set_mode((1200, 400))
        temp_surf.blit(instructions_image, (5,30))
        pygame.display.update()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.QUIT:
                    exit()
            pygame.display.update()

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

            pygame.display.update()
            #clock.tick()

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

            pygame.display.update()
            #clock.tick()

        display = pygame.display.set_mode((5+self.board_size*35, 5+self.board_size*35))
        pygame.display.set_caption('Play Minesweeper!')
        user = UI(display)
        user.start_game(self.board_size, number_of_mines)

    def start_game(self,board_size,number_of_mines):
        """
        Runs the start of the game, calls to initialize creation of a game board

        @pre Expects valid user input to be passed into launch.
        @param
            board_size: int value such that 2 <= board_size <= 39 to set an nxn board size
            number_of_mines: int value such that number_of_mines = (nxn) - 1
        @post Initializes a screen for user to play minesweeper based on params passed in by user
        @return None
        """
        click_sound=pygame.mixer.Sound("src/Tiny Button Push-SoundBible.com-513260752.wav")
        clock = pygame.time.Clock()
        self.board_size = int(board_size)
        self.number_of_mines = int(number_of_mines)
        game_win=False

        game_board = Gameboard(board_size, number_of_mines, self.display)

        #clock = pygame.time.Clock() #adds clock imported from pygame

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
                    click_sound.play()
                    position = pygame.mouse.get_pos()
                    try:
                        game_board.detect_location()
                    except Exception as statement:
                        word = str(statement)
                        running = False
                        break
                if ((event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 3)):
                    position = pygame.mouse.get_pos()
                    try:
                        game_board.call_flag()
                    except Exception as statement:
                        word = str(statement)
                        running = False
                        game_win= True
                        break
            game_board.draw()
            #pygame.display.update()

        #end game screen
        if not game_win:
            pygame.font.init()
            end_game_font = pygame.font.SysFont('Helvetica', 40)
            temp_surf = pygame.display.set_mode((1200, 100))
            font_surf = end_game_font.render(word, True, (250, 250, 250))
            temp_surf.blit(font_surf, (5,30))
            pygame.display.update()

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
