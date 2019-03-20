import pygame
from src.Gameboard import Gameboard
from src.GUIElements import TextInput, ButtonInput, MessageBox, Toggle,Clock
import time 
from random import randint

TestBoardSize = 15
MaxBoardSize = 25
UIColumnWidth = 225
UIHeight = 575

class UI:
    """
    The UI class creates UI elements, such as input boxes, buttons, toggles, and message boxes,
    for the user to see and interact with.
    """
   
    def __init__(self, display):
        """
        Creates the UI object to hold all other UI elements and to
        handle input.
        
        Arguments:
            display {pygame surface} -- The surface the textbox will be drawn on.
        """

        self.display = display
        #Normal mode is 0. Hard mode is 1
        self.mode = 0
        self.CheatModeEnabled = False
         
    def launch(self):
        """
        Initial launch of the game.
        Starts the music.
        Sets the size of the window and starts a new game.
        """

        pygame.mixer.music.load("src/sandstorm.mp3")
        pygame.mixer.music.set_volume(4)
        pygame.mixer.music.play(-1)

        pygame.font.init()
        surface = pygame.display.set_mode((UIColumnWidth + TestBoardSize * 35, 5 + TestBoardSize * 35))
        pygame.display.update()
        self.startGame(TestBoardSize, TestBoardSize, TestBoardSize, True)

    def startGame(self, width, height, bombs, firstGame):
        """
        Creates a new gameboard and clears the old one.
        Draws the UI and handles all input.
        
        Arguments:
            width {int} -- The width of the game board in tiles.
            height {int} -- The height of the game board in tiles.
            bombs {int} -- The number of bombs to place on the board.
            firstGame {bool} -- True if this is the first game played for this session.
        """

        click_sound=pygame.mixer.Sound("src/Tiny Button Push-SoundBible.com-513260752.wav")
        self.Clock = Clock(25 + width * 35, 500, self.display)
        
        #Dont clear the board if this is the initial game
        if(not firstGame):
            self.clearBoard()

        #The game just started, so isGameOver is false
        self.isGameOver = False

        #Create gameboard, draw UI, and resize the window to conform to gameboard size
        self.gameBoard = Gameboard(width, height, bombs, self.display)
        surface = pygame.display.set_mode((UIColumnWidth + width * 35, max(5 + height * 35, UIHeight)))
        self.drawUI(width, height, bombs)

        #Display a message explaining each mode.
        if self.mode == 0:
            self.PrintMessage(["Normal Mode", "is normal", "Minesweeper", ""])
        if self.mode == 1:
            self.PrintMessage(["Hard Mode", "randomizes", "the mines", "periodically"])

        #Set the clock offset and update the gameboard.
        self.Clock.offset = time.clock()
        self.gameBoard.update_board(self.display)

        running = True
        while(running):
            for event in pygame.event.get():

                #if you quit the window, exit the game
                if event.type == pygame.QUIT:
                    exit()

                #For every event, check if the event affects the inputs
                self.GetInput(event)

                if not self.isGameOver and not self.CheatModeEnabled:

                    #Detect left click on the location of the click
                    if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):

                        click_sound.play()
                        #if gameBoard throws an exception, meaning you either won or lost, end the game
                        try:
                            coords = self.gameBoard.detect_location()
                            if coords is not None:
                                self.gameBoard.on_left_click(coords[0], coords[1], self.display)
                                #if hard mode is enabled, then 25% chance to shuffle tiles
                                if self.mode == 1:
                                    if randint(0, 99) <= 25:
                                        self.gameBoard.shuffle_tiles()
                        except Exception as thrown:
                            self.EndGame(thrown)

                    #Detect right click on the location of the right click
                    if ((event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 3)):

                        #if gameBoard throws an exception, meaning you either won or lost, end the game
                        try:
                            coords = self.gameBoard.detect_location()
                            if coords is not None:
                                self.gameBoard.on_right_click(coords[0], coords[1], self.display)
                                #if hard mode is enabled, then 25% chance to shuffle tiles
                                if self.mode == 1:
                                    if randint(0, 99) <= 25:
                                        self.gameBoard.shuffle_tiles()
                        except Exception as thrown:
                            self.EndGame(thrown)

            #Update the input every loop
            self.DrawInput()
            
            if not self.CheatModeEnabled:
                #if UI has a gameboard and the game is not over, draw the board
                if hasattr(self, "gameBoard") and not self.isGameOver:
                    self.gameBoard.update_board(self.display)

            #Refresh the screen
            pygame.display.update()
        
    def DrawInput(self):
        """
        Draws each of the UI elements on the screen.
        """

        #Draw the text inputs
        self.HeightInput.draw(self.display)
        self.WidthInput.draw(self.display)
        self.BombInput.draw(self.display)

        #Draw the buttons
        self.NewGameButton.draw(self.display)
        self.CheatButton.draw(self.display)

        #Draw the message boxes
        for Message in self.Messages:
            Message.draw(self.display)

        #Draw the toggles
        self.NormalToggle.draw()
        self.HardToggle.draw()

        #Only draw the clock if the game is not over.
        if not self.isGameOver:
            self.Clock.draw_clock(time.clock())

    def GetInput(self, event):
        """
        Sends the pygame event to each interactable UI element
        to see if the event affects that element.
        
        Arguments:
            event {pygame event} -- The event that occurred, e.g., mouse click, typing, deleting, etc.
        """

        self.BombInput.eventControl(event, self)
        self.HeightInput.eventControl(event, self)
        self.WidthInput.eventControl(event, self)

        self.NewGameButton.eventControl(event, self)
        self.CheatButton.eventControl(event, self)

        self.NormalToggle.eventControl(event, self)
        self.HardToggle.eventControl(event, self)

    def drawUI(self, width, height, bombs):
        """
        Creates and draws each UI element at the correct position.
        
        Arguments:
            width {int} -- The width of the game board in tiles.
            height {int} -- The height of the game board in tiles.
            bombs {int} -- The number of bombs to place on the board.
        """

        #Create the Clock.
        self.Clock = Clock(25 + width * 35, 500, self.display)

        #Create 4 message boxes.
        self.Message1 = MessageBox(25 + width * 35, 310, "", self.display)
        self.Message2 = MessageBox(25 + width * 35, 342, "", self.display)
        self.Message3 = MessageBox(25 + width * 35, 374, "", self.display)
        self.Message4 = MessageBox(25 + width * 35, 406, "", self.display)

        self.Messages = [self.Message1, self.Message2, self.Message3, self.Message4]

        #Create two toggles, one Normal and one hard. Default to normal mode
        self.NormalToggle = Toggle("NORMAL", 25 + width * 35, 160, self.display, not self.mode)
        self.HardToggle = Toggle("HARD", 25 + width * 35, 210, self.display, self.mode)

        #Link the toggle elements together, so when you toggle one, the other won't stay active
        self.NormalToggle.SetOtherToggle(self.HardToggle)
        self.HardToggle.SetOtherToggle(self.NormalToggle)

        #Create the new game button
        self.NewGameButton = ButtonInput("New Game", 25 + width * 35, 260, self.display, "lightgreen", self.NewGame)
        
        #Create the Cheat Mode button
        self.CheatButton = ButtonInput("Cheat Mode", 25 + width * 35, 456, self.display, "lightblue", self.ToggleCheatMode)
        
        #Create each text input. They need to be in this order to tab to the next one.
        self.BombInput = TextInput("Bombs: ", str(bombs), 25 + width * 35, 110, self.display, None)
        self.HeightInput = TextInput("Height: ", str(height), 25 + width * 35, 60, self.display, self.BombInput)
        self.WidthInput = TextInput("Width: ", str(width), 25 + width * 35, 10, self.display, self.HeightInput)

    def clearBoard(self):
        if hasattr(self, "gameBoard"):
            del self.gameBoard
        self.display.fill(pygame.Color("black"))

    def NewGame(self):
        """
        Called when the "New Game" button is pressed,
        or when the suer presses enter when typing in a text box,
        or if the user tabs out of the last input field.

        Checks the input of the text boxes and then starts a new game if the inputs are valid.
        """

        #Get the values of the inputs
        width = int(self.WidthInput.value) if self.WidthInput.value != "" else 0
        height = int(self.HeightInput.value) if self.HeightInput.value != "" else 0
        bombs = int(self.BombInput.value) if self.BombInput.value != "" else 0

        #Check to see if the input is valid
        if self.GoodInput(width, height, bombs):
            self.CheatModeEnabled = False
            self.Clock.offset = time.clock()
            self.startGame(width, height, bombs, False)
        
    def GoodInput(self, width, height, bombs):
        """
        Verifies the input of the textbox inputs.
        Width must be between 2 and 25.
        Height must be between 2 and 25.
        Bombs must be between 1 and Width * Height - 1.
        Prints an error message if any of these conditions are not met.
        
        Arguments:
            width {int} -- The width of the game board in tiles.
            height {int} -- The height of the game board in tiles.
            bombs {int} -- The number of bombs to place on the board.
        
        Returns:
            bool -- True if all inputs are valid. False if any of them fail.
        """

        if width > 25 or width < 2:
            self.PrintMessage(["Invalid Width:", "Input a value", "Between", "2 and 25"])
            return False
        if height > 25 or height < 2:
            self.PrintMessage(["Invalid Height:", "Input a value", "Between", "2 and 25"])
            return False
        if bombs > width * height - 1 or bombs < 1:
            self.PrintMessage(["Invalid Bombs:", "Input a value", "Between", "1 and " + str(width * height - 1)])
            return False
        return True

    def PrintMessage(self, strings):
        """
        Updates the text of each of the UI message elements
        and draws them on the screen.
        
        Arguments:
            strings {string array} -- A list of the messages to be displayed.
        """

        for i in range(len(strings)):
            self.Messages[i].UpdateText(strings[i])

    def SetGameMode(self, mode):
        """
        Sets the game mode to the toggle selected and displays
        information about the mode.
        
        Arguments:
            mode {bool} -- The game mode to use to display the correct message.
        """

        if mode == 0:
            self.PrintMessage(["Normal Mode", "is normal", "Minesweeper", ""])
        if mode == 1:
            self.PrintMessage(["Hard Mode", "randomizes", "the mines", "periodically"])
        self.mode = mode

    def EndGame(self, exceptionThrown):
        """
        Reveals all tiles on the gameboard.
        Deletes the board, so the user cannot interact with it.
        Prints a message in the message boxes with the end games state.
        
        Arguments:
            exceptionThrown {string} -- The value of the exception thrown.
                                        Used to determine which message to print.
        """

        #Reveal all tiles on the board and delete the board.
        if(hasattr(self,"gameBoard")):
            self.display.fill((0, 0, 0))
            self.gameBoard.update_board(self.display)
            self.gameBoard.RevealAll(self.display)
            del self.gameBoard
        pygame.display.flip


        #Game is over, so take no input on the gameboard.
        self.isGameOver = True

        #Print the game ending message
        if str(exceptionThrown) == "Congratulations, you win!":
            self.PrintMessage(["Congratulations!", "You Win!", "Total Time:", self.Clock.mytime + " seconds!"])
        elif str(exceptionThrown) == "Oh no! You exploded!":
            self.PrintMessage(["Oh No!", "You Lose!", "Click New Game", "to play again"])

    def ToggleCheatMode(self):
        """
        Toggles the cheat mode button, and enables cheat mode on the gameboard.
        """

        if hasattr(self, "gameBoard"):
            self.CheatModeEnabled = not self.CheatModeEnabled
            self.CheatButton.Toggle()
            self.gameBoard.ToggleCheatMode(self.CheatButton.isActive, self.display)

