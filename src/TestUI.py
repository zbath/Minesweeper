import pygame
from src.Gameboard import Gameboard
from src.GUIElements import TextInput, ButtonInput, MessageBox, Toggle

TestBoardSize = 15
MaxBoardSize = 25
UIColumnWidth = 225
UIHeight = 500

#Class to handle creating input boxes and buttons, also to handle taking input
class UI:
    #Pass the game surface as "display" for the UI to use
    def __init__(self, display):
        self.display = display

        #Normal mode is 0. Hard mode is 1
        self.mode = 0

    #Sets the window size and starts the game
    def launch(self):
        pygame.font.init()

        #This sets the window size.
        surface = pygame.display.set_mode((UIColumnWidth + TestBoardSize * 35, 5 + TestBoardSize * 35))
        pygame.display.flip()
        self.startGame(TestBoardSize, TestBoardSize, TestBoardSize, True)

    #Creates the initial game board, draws the UI, and handles all input
    def startGame(self, width, height, bombs, firstGame):
        #Dont clear the board if this is the initial game
        if(not firstGame):
            self.clearBoard()

        #The game is not over, so isGameOver is false
        self.isGameOver = False

        #Create gameboard, draw UI, and resize the window to conform to gameboard size
        self.gameBoard = Gameboard(width, height, bombs, self.display)
            ## add mode and height parameter when the function can handle it
            ## self.gameBoard = Gameboard(width, height, bombs, self.display, self.mode)
            ## doing it this way will allow the mode to persist throughout the lifetime
            ## of the gameboard, which is deleted when a new game is started
        surface = pygame.display.set_mode((UIColumnWidth + width * 35, max(5 + height * 35, UIHeight)))
        self.drawUI(width, height, bombs)

        #Event handling loop
        running = True
        self.gameBoard.update_board()
        while(running):
            for event in pygame.event.get():
                
                #if you quit the window, exit the game
                if event.type == pygame.QUIT:
                    exit()

                #For every event, check if the event affects the inputs
                self.GetInput(event)
                
                #If the game is not over handle the events thrown from the gameboard
                ##Might have to change this based on what is changed from the win and lose condition function
                if not self.isGameOver:

                    #Detect left click on the location of the click
                    if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                        
                        #if gameBoard throws an exception, meaning you either won or lost, end the game
                        try:
                            coords = self.gameBoard.detect_location()
                            if coords is not None:
                                self.gameBoard.on_left_click(coords[0], coords[1])
                        except Exception as thrown:
                            print(f'Caught Exception: {str(thrown)} \nEnding Game')
                            self.EndGame(thrown)
                    
                    #Detect right click on the location of the right click
                    if ((event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 3)):
                        
                        #if gameBoard throws an exception, meaning you either won or lost, end the game
                        try:
                            coords = self.gameBoard.detect_location()
                            if coords is not None:
                                self.gameBoard.on_right_click(coords[0], coords[1])
                            else:
                                self.gameBoard.shuffle_tiles()
                        except Exception as thrown:
                            print(f'Caught Exception: {str(thrown)} \nEnding Game')
                            self.EndGame(thrown)

            #Update the input every loop
            self.DrawInput()

            #if UI has a gameboard and the game is not over, draw the board
            if hasattr(self, "gameBoard") and not self.isGameOver:
                self.gameBoard.update_board()

            #Refresh the screen
            pygame.display.flip()

    #Draw each of the UI elements on the screen
    def DrawInput(self):
        #Draw the text inputs
        self.HeightInput.draw(self.display)
        self.WidthInput.draw(self.display)
        self.BombInput.draw(self.display)

        #Draw the buttons
        self.NewGameButton.draw(self.display)
        self.shuffleButton.draw(self.display)

        #Draw the message boxes
        for Message in self.Messages:
            Message.draw(self.display)
        
        #Draw the toggles
        self.NormalToggle.draw()
        self.HardToggle.draw()

    #Send the event to each input field to see if the event affects the input
    def GetInput(self, event):
        #send event to text inputs
        self.BombInput.eventControl(event, self)
        self.HeightInput.eventControl(event, self)
        self.WidthInput.eventControl(event, self)

        #send event to buttons
        self.NewGameButton.eventControl(event, self)
        self.shuffleButton.eventControl(event, self)

        #send event to toggles
        self.NormalToggle.eventControl(event, self)
        self.HardToggle.eventControl(event, self)

    #Creates the UI elements
    def drawUI(self, width, height, bombs):

        #create the message boxes. There are currently 4, but can add more if necessary 
        self.Message1 = MessageBox(25 + width * 35, 310, "", self.display)
        self.Message2 = MessageBox(25 + width * 35, 342, "", self.display)
        self.Message3 = MessageBox(25 + width * 35, 374, "", self.display)
        self.Message4 = MessageBox(25 + width * 35, 406, "", self.display)

        self.Messages = [self.Message1, self.Message2, self.Message3, self.Message4]

        #Create two toggles, one Normal and one hard. Default to normal mode
        self.NormalToggle = Toggle("NORMAL", 25 + width * 35, 160, self.display, True)
        self.HardToggle = Toggle("HARD", 25 + width * 35, 210, self.display, False)

        #Link the toggle elements together, so when you toggle one, the other won't stay active
        self.NormalToggle.SetOtherToggle(self.HardToggle)
        self.HardToggle.SetOtherToggle(self.NormalToggle)

        #Create the new game button
        self.NewGameButton = ButtonInput("New Game", 25 + width * 35, 260, self.display, "lightgreen", self.NewGame)
        
        #Create the shuffle button
        self.shuffleButton = ButtonInput("Shuffle Mines", 25 + width * 35, 456, self.display, "lightblue", self.ShuffleMines)
        
        #Create each text input. They need to be in this order to tab to the next one.
        self.BombInput = TextInput("Bombs: ", str(bombs), 25 + width * 35, 110, self.display, None)
        self.HeightInput = TextInput("Height: ", str(height), 25 + width * 35, 60, self.display, self.BombInput)
        self.WidthInput = TextInput("Width: ", str(width), 25 + width * 35, 10, self.display, self.HeightInput)

    #Deletes the game board and draws a black rectangle over the whole screen
    def clearBoard(self):
        if hasattr(self, "gameBoard"):
            del self.gameBoard
        self.display.fill(pygame.Color("black"))

    #Called when the "New Game" button is pressed, or if the user presses enter when typing in a
    #text input field, or if the user tabs out of the last input field.
    def NewGame(self):

        #Get the values of the inputs
        width = int(self.WidthInput.value) if self.WidthInput.value != "" else 0
        height = int(self.HeightInput.value) if self.HeightInput.value != "" else 0
        bombs = int(self.BombInput.value) if self.BombInput.value != "" else 0
        
        #Check to see if the input is valid
        if self.GoodInput(width, height, bombs):
            #Clear the board by deleting the gameboard, and drawing a filled rectagle over the top,
            #then Draw a new board
            self.startGame(width, height, bombs, False)

    #Checks if the input given is valid
    def GoodInput(self, width, height, bombs):
        if width > 25 or width < 2:
            self.PrintMessage(["Invalid Width:", "Input a value", "Between", "2 and 25"])
            return False
        if height > 25 or height < 2:
            self.PrintMessage(["Invalid Height:", "Input a value", "Between", "2 and 25"])
            print("invalid height")
            return False
        if bombs > width * height - 1 or bombs < 1:
            self.PrintMessage(["Invalid Bombs:", "Input a value", "Between", "1 and " + str(width * height - 1)])
            return False
        return True

    #Updates the text of every message box
    def PrintMessage(self, strings):
        for i in range(len(strings)):
            self.Messages[i].UpdateText(strings[i])

    #Sets the game mode to the toggle selected and prints info about the mode
    def SetGameMode(self, mode):
        if mode == 0:
            self.PrintMessage(["Normal Mode", "is normal", "Minesweeper", ""])
        if mode == 1:
            self.PrintMessage(["Hard Mode", "randomizes", "the mines", "periodically"])
        self.mode = mode

    ##Called to shuffle the mines. This is for testing only. In the final product, the function should be called
    ## from the gameboard
    def ShuffleMines(self):
        print("Mines have been shuffled")
        ##Whatever you end up calling the shuffle mine function
        ##self.gameBoard.shuffleMines()
    
    #Reveals all tiles on the gameboard and redraws it.
    #Deletes the board, so the user cannot interact with it.
    #Prints a message in the message boxes.
    def EndGame(self, exceptionThrown):
        ##Whatever you end up calling the reveal all function
        ##self.gameBoard.RevealAll()

        #Draws the revealed board
        self.gameBoard.update_board()
        pygame.display.flip()
        
        del self.gameBoard

        #Game is over, so take no input on the gameboard.
        self.isGameOver = True

        #Print the game ending message
        ##These conditions will probably change depending on how win and lose condition functions work.
        if str(exceptionThrown) == "Congratulations, you win!":
            self.PrintMessage(["Congratulations!", "You Win!", "Click New Game", "to play again"])
        elif str(exceptionThrown) == "Oh no! You exploded!":
            self.PrintMessage(["Oh No!", "You Lose!", "Click New Game", "to play again"])


