#This starts the display which will call UI and Gameboard
import pygame

from src.Styles import Styles
from src.Gameboard import Gameboard

class Game:
    def __init__(self, display):
        self.display = display

    def loop(self):
        clock = pygame.time.Clock() #adds clock imported from pygame

        while True: #sets the main game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            Gameboard.draw()

        pygame.display.update()
        clock.tick(30)

    display = pygame.display.set_mode(
        (Styles['game']['width'],
        Styles['game']['width'])
    )
    pygame.display.set_caption('Play PoopScoop!')

