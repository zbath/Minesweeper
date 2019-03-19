import pygame
import src.TestUI as TestUI
import time

FONT = pygame.font.Font(None, 32)
InactiveColor = pygame.Color("white")
ActiveColor = pygame.Color("red")

#Class to create a text input field that is interactable
class TextInput:
    def __init__(self, text, value, x, y, display, nextInput):
        self.text = text
        self.isActive = False
        self.value = value
        self.rect = pygame.Rect(x, y, 175, 32)
        self.color = InactiveColor
        self.textBox = FONT.render(self.text + self.value, True, self.color)
        self.display = display
        self.nextInput = nextInput

    #Handles all events dealing with the text input
    def eventControl(self, event, UI):
        #If the event is a click
        if event.type == pygame.MOUSEBUTTONDOWN:
            #If the click is on the input box, set the box to be active and clear input
            if self.rect.collidepoint(event.pos):
                self.isActive = True
                self.clearInput()
            #if the click is not on the text box, then set active to false
            else:
                self.isActive = False

            #Changes the color of the input to the active color and updates the text
            self.setActive(self.isActive)
        
        #If the event is a keypress
        if event.type == pygame.KEYDOWN:

            #if the text input box is active
            if self.isActive:

                #if the user hits the enter key, then start a new game
                if event.key == pygame.K_RETURN:
                    #Start a new game
                    UI.NewGame()
                    print("NewGame")
                
                #if the user hits the backspace key, then delete the last character in self.value and update text
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.value) > 0:
                        self.value = self.value[:-1]
                        self.UpdateText()

                #enables the user to tab from one input to the next
                elif event.key == pygame.K_TAB:
                    self.NextInput()

                    #if the user tabs from the last input box, create a new game
                    if self.text == "Bombs: ":
                        UI.NewGame()
                        print("NewGame")

                #if the user enters a digit, append the digit to self.value
                elif pygame.key.name(event.key).isdigit():
                    #limits the input to a length of 4
                    if len(self.value) < 4:
                        self.value += pygame.key.name(event.key)
                
                #Update the text
                self.UpdateText()
   
    #Called for the initial drawing of the text box
    def draw(self, display):
        display.blit(self.textBox, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(display, self.color, self.rect, 2)

    #Clears self.value and updates the text
    def clearInput(self):
        self.value = ""
        self.UpdateText()

    #Sets the current text box to inactive and the next input to active
    def NextInput(self):
        self.setActive(False)
        if(self.nextInput):
            self.nextInput.setActive(True)
            self.nextInput.clearInput()
    
    #Sets the text input's active state equal to "state" and changes the color and updates text
    def setActive(self, state):
        self.isActive = state
        self.color = ActiveColor if state else InactiveColor
        self.UpdateText()

    #Clears the current value of text by drawing a black box over the value,
    #then draws the text on top
    def UpdateText(self):
        pygame.draw.rect(self.display, pygame.Color("black"), self.rect, 0)
        self.textBox = FONT.render(self.text + self.value, True, self.color)

#Class to create a button that is interactable
class ButtonInput:
    def __init__(self, text, x, y, display, color, eventFunction):
        self.text = text
        self.rect = pygame.Rect(x, y, 175, 32)
        self.color = pygame.Color(color)
        self.textBox = FONT.render(self.text, True, pygame.Color("black"))
        self.display = display
        self.eventFunction = eventFunction
    
    #Handles the events passed to the button
    def eventControl(self, event, UI):
        #if the user clicks on the button, clear the old board and create a new one
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                #Draw a new board over the new one
                self.eventFunction()
                #print("NewGame")
    
    #Called to initially draw the button
    def draw(self, display):
        display.blit(self.textBox, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(display, self.color, self.rect, 0)
        display.blit(FONT.render(self.text, True, pygame.Color("black")), (self.rect.x + 5, self.rect.y + 5))   

#Class to create a message box that has no user interaction
class MessageBox:
    def __init__(self, x, y, text, display):
        self.text = text
        self.rect = pygame.Rect(x, y, 175, 32)
        self.color = pygame.Color("white")
        self.textBox = FONT.render(self.text, True, pygame.Color("white"))
        self.display = display
    
    #The initial draw of the message box.
    def draw(self, display):
        display.blit(self.textBox, (self.rect.x + 5, self.rect.y + 5))
        self.UpdateText(self.text)

    #Update the text, draw a black rectangle over the box, then render the text
    def UpdateText(self, text):
        self.text = text
        pygame.draw.rect(self.display, pygame.Color("black"), self.rect, 0)
        self.display.blit(FONT.render(self.text, True, pygame.Color("white")), self.rect)   

#Class to create a toggle that the user can interact with
class Toggle:
    def __init__(self, text, x, y, display, isActive):
        self.isActive = isActive
        self.text = text + "   X" if isActive else text
        self.rect = pygame.Rect(x, y, 175, 32)
        self.color = ActiveColor if isActive else InactiveColor
        self.textBox = FONT.render(self.text, True, self.color)
        self.display = display
        self.isActive = isActive
        self.otherToggle = None

    #Handles events on the toggle
    def eventControl(self, event, UI):
        #If the event is a click
        if event.type == pygame.MOUSEBUTTONDOWN:
            #If the click is on the input box, set the toggle to active and the other toggle to inactive
            if self.rect.collidepoint(event.pos) and not self.isActive:
                self.Toggle(UI)

    #The initial draw of the toggle
    def draw(self):
        self.display.blit(self.textBox, (self.rect.x + 5, self.rect.y + 5))

    #Sets the link to the other toggle.
    def SetOtherToggle(self, otherToggle):
        self.otherToggle = otherToggle

    #Set the current toggle to active and the other toggle to inactive and sets the mode
    def Toggle(self, UI):
        #Set the mode of the next game to be created
        mode = 0 if self.text == "NORMAL" else 1
        UI.SetGameMode(mode)
        
        #Activate the current toggle
        self.text += "   X"
        self.color = ActiveColor
        self.isActive = not self.isActive
        self.UpdateToggle()        

        #Deactivate the other toggle
        self.otherToggle.text = self.otherToggle.text[:-4]
        self.otherToggle.color = InactiveColor
        self.otherToggle.isActive = False
        self.otherToggle.UpdateToggle()

    #Updates the toggle to be drawn
    def UpdateToggle(self):
        pygame.draw.rect(self.display, pygame.Color("black"), self.rect, 0)
        self.textBox = FONT.render(self.text, True, self.color)

class Clock:
    def __init__(self, x, y, display):
        self.clock_font  = pygame.font.SysFont('Helvetica', 26)
        self.secondsTimer = pygame.Rect(x, y, 120, 30)
        self.myClock = pygame.Rect(x, y + 24, 120, 30)
        self.display = display
        self.start= time.clock()
    
    def draw_clock(self,start):
        self.start = start
        self.elapsed = time.clock() - start
        self.mytime = str(int(start))
        pygame.draw.rect(self.display, (112, 128, 144), self.myClock)
        pygame.draw.rect(self.display, (112, 128, 144), self.secondsTimer)
        text2= self.clock_font.render( "Time: ", True, (250, 250, 250))
        text = self.clock_font.render( self.mytime + " seconds", True, (250, 250, 250))
        self.display.blit(text, self.myClock)
        self.display.blit(text2, self.secondsTimer)
        
    
    