import pygame
import time

FONT = pygame.font.Font(None, 32)
InactiveColor = pygame.Color("white")
ActiveColor = pygame.Color("red")

class TextInput:
    """
    The TextInput class creates an interactable text box that the user can manipulate.
    """

    def __init__(self, text, value, x, y, display, nextInput):
        """
        Creates the TextInput UI object
        
        Arguments:
            text {string} -- This is the initial text that will be placed in the text box.
            value {string} -- This is the number as a string entered by the user.
            x {int} -- The x position of the screen to place the textbox.
            y {int} -- The y position of the screen to place the textbox.
            display {pygame surface} -- The surface the textbox will be drawn on.
            nextInput {TextInput} -- The next textbox, so you can tab into the next entry.
        """

        self.text = text
        self.isActive = False
        self.value = value
        self.rect = pygame.Rect(x, y, 175, 32)
        self.color = InactiveColor
        self.textBox = FONT.render(self.text + self.value, True, self.color)
        self.display = display
        self.nextInput = nextInput

    def eventControl(self, event, UI):
        """
        Handles all pygame events for the TextInput.
        
        Arguments:
            event {pygame event} -- The event that occurred, e.g., mouse click, typing, deleting, etc.
            UI {UI object} -- The UI object this textbox is an attribute of, to call UI functions.
        """

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.isActive = True
                self.clearInput()
            else:
                self.isActive = False
            self.setActive(self.isActive)
        
        if event.type == pygame.KEYDOWN:
            if self.isActive:
                if event.key == pygame.K_RETURN:
                    UI.NewGame()
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.value) > 0:
                        self.value = self.value[:-1]
                        self.UpdateText()
                elif event.key == pygame.K_TAB:
                    self.NextInput()
                    if self.text == "Bombs: ":
                        UI.NewGame()
                elif pygame.key.name(event.key).isdigit():
                    if len(self.value) < 4:
                        self.value += pygame.key.name(event.key)
                self.UpdateText()
   
    def draw(self, display):
        """
        Draws the textbox on the screen.
        
        Arguments:
            display {pygame surface} -- The surface the textbox is drawn on.
        """

        display.blit(self.textBox, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(display, self.color, self.rect, 2)

    def clearInput(self):
        """
        Clears the value of the textbox.
        """

        self.value = ""
        self.UpdateText()

    def NextInput(self):
        """
        Sets the current textbox to inactive and activates the next textbox if it exists.
        Essentially, this allows for tabbing from one entry to another.
        """

        self.setActive(False)
        if(self.nextInput):
            self.nextInput.setActive(True)
            self.nextInput.clearInput()
    
    def setActive(self, state):
        """
        Changes the active state of the textbox.
        
        Arguments:
            state {boolean} -- The value to assign to isActive.
        """

        self.isActive = state
        self.color = ActiveColor if state else InactiveColor
        self.UpdateText()

    def UpdateText(self):
        """
        Updates the value of the text and draws it in the textbox.
        """

        pygame.draw.rect(self.display, pygame.Color("black"), self.rect, 0)
        self.textBox = FONT.render(self.text + self.value, True, self.color)

class ButtonInput:
    """
    The ButtonInput class creates an interactable button for the user to click.
    """

    def __init__(self, text, x, y, display, color, eventFunction, active=False):
        """
        Creates a ButtonInput that the user can click.
        
        Arguments:
            text {string} -- The text to be displayed inside the button.
            x {int} -- The x position of the screen to place the textbox.
            y {int} -- The y position of the screen to place the textbox.
            display {pygame surface} -- The surface to draw the button on.
            color {(int, int, int)} -- The color of the button.
            eventFunction {function} -- The function to be called when the button is clicked.
        
        Keyword Arguments:
            active {bool} -- Used for the cheat mode button to implement a toggle. (default: {False})
        """

        self.text = text
        self.rect = pygame.Rect(x, y, 175, 32)
        self.color = pygame.Color(color)
        self.textBox = FONT.render(self.text, True, pygame.Color("black"))
        self.display = display
        self.eventFunction = eventFunction
        self.isActive = active
    
    def eventControl(self, event, UI):
        """
        Handles all pygame events for the ButtonInput.
        
        Arguments:
            event {pygame event} -- The event that occurred, e.g., mouse click, typing, deleting, etc.
            UI {UI object} -- The UI object this textbox is an attribute of, to call UI functions.
        """

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.eventFunction()
    
    def draw(self, display):
        """
        Draws the Button on the surface.
        
        Arguments:
            display {pygame surface} -- The surface for the button to be drawn on.
        """

        display.blit(self.textBox, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(display, self.color, self.rect, 0)
        display.blit(FONT.render(self.text, True, pygame.Color("black")), (self.rect.x + 5, self.rect.y + 5))   

    def Toggle(self):
        """
        Sets the active state of the button to the opposite of what it was and updates the text.
        """

        if(not self.isActive):
            self.isActive = True
            self.text += "   X"
            self.draw(self.display)
        else:
            self.text = self.text[:-4]
            self.isActive = False
            self.draw(self.display)


class MessageBox:
    """
    The MessageBox class creates a message box to display text to the user.
    """

    def __init__(self, x, y, text, display):
        """
        Creates a ButtonInput, so the user can see a message.
        
        Arguments:
            x {int} -- The x position of the screen to place the textbox.
            y {int} -- The y position of the screen to place the textbox.
            text {string} -- The text to be displayed to the user.
            display {pygame surface} -- The surface to draw the message box on.
        """

        self.text = text
        self.rect = pygame.Rect(x, y, 175, 32)
        self.color = pygame.Color("white")
        self.textBox = FONT.render(self.text, True, pygame.Color("white"))
        self.display = display
    
    def draw(self, display):
        """
        Draws the message box on the surface.
        
        Arguments:
            display {pygame surface} -- The surface to draw the message box on.
        """

        display.blit(self.textBox, (self.rect.x + 5, self.rect.y + 5))
        self.UpdateText(self.text)

    def UpdateText(self, text):
        """
        Updates the value of text and draws it in the message box.
        
        Arguments:
            text {string} -- The text to display to the user.
        """

        self.text = text
        pygame.draw.rect(self.display, pygame.Color("black"), self.rect, 0)
        self.display.blit(FONT.render(self.text, True, pygame.Color("white")), self.rect)   

class Toggle:
    """
    The Toggle class creates an interactable toggle for the user to click.
    """

    def __init__(self, text, x, y, display, isActive):
        """
        Creates a Toggle that the user can click.
        
        Arguments:
            text {string} -- The text to be displayed inside the toggle.
            x {int} -- The x position of the screen to place the textbox.
            y {int} -- The y position of the screen to place the textbox.
            display {pygame surface} -- The surface to draw the toggle on.
            isActive {bool} -- Whether the toggle is enabled or not.
        """

        self.isActive = isActive
        self.text = text + "   X" if isActive else text
        self.rect = pygame.Rect(x, y, 175, 32)
        self.color = ActiveColor if isActive else InactiveColor
        self.textBox = FONT.render(self.text, True, self.color)
        self.display = display
        self.isActive = isActive
        self.otherToggle = None

    def eventControl(self, event, UI):
        """
        Handles all pygame events for the Toggle.
        
        Arguments:
            event {pygame event} -- The event that occurred, e.g., mouse click, typing, deleting, etc.
            UI {UI object} -- The UI object this textbox is an attribute of, to call UI functions.
        """

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and not self.isActive:
                self.Toggle(UI)

    def draw(self):
        """
        Draws the Toggle on the surface.
        """

        self.display.blit(self.textBox, (self.rect.x + 5, self.rect.y + 5))

    def SetOtherToggle(self, otherToggle):
        """
        Sets the value of the other toggle.
        This is used when the user clicks on one toggle, then
        the "otherToggle" is set to inactive.
        
        Arguments:
            otherToggle {Toggle object} -- The toggle to disable when the current toggle is clicked.
        """

        self.otherToggle = otherToggle

    def Toggle(self, UI):
        """
        Sets the current toggle to active, and the otherToggle to inactive.
        Changes the color and text of the toggles.
        This also determines the game mode to be played.
        
        Arguments:
            UI {UI object} -- The UI object this textbox is an attribute of, to call UI functions.
        """

        mode = 0 if self.text == "NORMAL" else 1
        UI.SetGameMode(mode)
        
        self.text += "   X"
        self.color = ActiveColor
        self.isActive = not self.isActive
        self.UpdateToggle()        

        self.otherToggle.text = self.otherToggle.text[:-4]
        self.otherToggle.color = InactiveColor
        self.otherToggle.isActive = False
        self.otherToggle.UpdateToggle()

    def UpdateToggle(self):
        """
        Updates the value of the toggle and draws it on the surface.
        """

        pygame.draw.rect(self.display, pygame.Color("black"), self.rect, 0)
        self.textBox = FONT.render(self.text, True, self.color)
#Class is responsible for intializing a clock and its placement according to the gamescreen. 
#Clock font is specified and the clock itself functions based on the start and offset integer variables
#The start integer will increase as the program runs and when new game is pressed the value that offset takes 
#will be exactly the same as starts, therefore start - offset will reset the clock to a value of 0 
class Clock:
    """
    The Clock class creates a clock to be displayed to the user.
    """

    def __init__(self, x, y, display):
        """
        Creates a Clock that the user can see.
        
        Arguments:
            x {int} -- The x position of the screen to place the textbox.
            y {int} -- The y position of the screen to place the textbox.
            display {pygame surface} -- The surface to draw the button on.
        """

        self.clock_font  = pygame.font.SysFont('Helvetica', 26)
        self.secondsTimer = pygame.Rect(x, y, 175, 30)
        self.myClock = pygame.Rect(x, y + 24, 175, 30)
        self.display = display
        self.mytime = 0
        self.start = 0
        self.offset = 0
    # This function is responsible for drawing the clock on the gameboard. 
    #pygrame.draw.rect will draw both rectangles and text/text2 will specify the words stated on the 
    #rectangles. Blit will simply display the text on the screen. 
    def draw_clock(self,start):
        """
        Updates the time on the clock and displays it to the user.
        
        Arguments:
            start {float} -- The time in seconds since the game was started.
        """

        self.mytime = str(int(start) - int(self.offset))
        pygame.draw.rect(self.display, (112, 128, 144), self.myClock)
        pygame.draw.rect(self.display, (112, 128, 144), self.secondsTimer)
        text2= self.clock_font.render( "Time: ", True, (250, 250, 250))
        text = self.clock_font.render( self.mytime + " seconds", True, (250, 250, 250))
        self.display.blit(text, self.myClock)
        self.display.blit(text2, self.secondsTimer)
        
    
    