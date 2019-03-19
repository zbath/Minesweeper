import pygame
import random

class windisplay:

    def __init__(self, board_size_x, board_size_y, display):
      self.run = True
      self.board_size_x=225+board_size_x*35
      self.board_size_y= max(5+board_size_y*35, 575)
      self.display=display

    def displayfireworks(self):
        #self.NewGameButton = ButtonInput("Restart game", (self.board_size_y/2)-100, 260, self.display, "lightgreen", self.NewGame)
        font =pygame.font.SysFont('comicsans', 50, True)
        text= font.render("You win!", 1, (250, 250, 250))
        screen_size=[self.board_size_x, self.board_size_y]
        firework0 = []
        BLACK_FADED = [0, 0, 0, 10]
        blackSurf = pygame.Surface(screen_size).convert_alpha()
        blackSurf.fill(BLACK_FADED)
        lifespan=300
        while self.run:
            self.display.blit(blackSurf, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            if random.randint(0, 101) < 10:
              firework0.append(firework(self.board_size_x, self.board_size_y, self.display))
            self.display.blit(self.display, (0,0))
            self.display.blit(text, (self.board_size_x/2-100, self.board_size_y/2))
            for element in firework0:
              element.update()
              element.display()
              if element.done():
                firework0.pop(firework0.index(element))
            pygame.display.update()
            #self.NewGameButton.draw(self.display)
            #lifespan-=1
        #pygame.quit()

class particle:

        gravity= 1

        def __init__(self, x, y, first, color_A, color_B, color_C, display):
          self.x=x
          self.y=y
          self.accel_x=0
          self.accel_y=0
          self.first=first
          self.life=200
          self.color_A=color_A
          self.color_B=color_B
          self.color_C=color_C
          self.window=display
          if self.first:
           self.vel_x=0
           self.vel_y=random.randint(-30, -20)
          else:
              self.vel_x=random.randint(-30, 30)
              self.vel_y=random.randint(-30, 30)


        def applyGravity(self):
          self.accel_y =particle.gravity

        def update(self):
         if not self.first:
            self.life -=10
            self.vel_x = round(self.vel_x * 0.85)
            self.vel_y = round(self.vel_y * 0.85)
         self.vel_x += self.accel_x
         self.vel_y += self.accel_y
         self.x += self.vel_x
         self.y += self.vel_y
         self.accel_y=0

        def redraw(self):
            if self.life > 0:
             pygame.draw.circle(self.window, (self.color_A, self.color_B, self.color_C), (self.x, self.y), 1)

        def done(self):
            if self.life <= 0:
                return True
            else:
                return False

class firework:

     def __init__(self, board_size_x, board_size_y, display):
       self.particle0=particle(random.randint(0, board_size_x), board_size_y-30, True, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), display)
       self.exploded=False
       self.particles=[]

     def createSubPar(self):
       for element in range(0, 99):
         tempPar = particle(self.particle0.x, self.particle0.y, False, self.particle0.color_A, self.particle0.color_B, self.particle0.color_C, self.particle0.window)
         self.particles.append(tempPar)

     def update(self):
        if not self.exploded:
         self.particle0.applyGravity()
         self.particle0.update()
         if self.particle0.vel_y == 0:
            self.exploded = True
            self.explode()
            #firework_explosion.play()
        else:
            for element in self.particles:
                element.applyGravity()
                element.update()
                if element.done():
                  self.particles.pop(self.particles.index(element))


     def explode(self):
          self.createSubPar()

     def display(self):
       if not self.exploded:
        self.particle0.redraw()
       else:
           for element in self.particles:
             element.redraw()

     def done(self):
         if self.exploded and len(self.particles) == 0:
            return True
         else:
             return False

# run = True
# screen_size=[500, 500]
# firework0 = []
# BLACK_FADED = [0, 0, 0, 10]
# blackSurf = pygame.Surface(screen_size).convert_alpha()
# blackSurf.fill(BLACK_FADED)
# while run:
#     window.blit(blackSurf, (0,0))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#     if random.randint(0, 301) < 10:
#       firework0.append(firework())
#     #window.fill((0, 0, 0)
#     window.blit(window, (0,0))
#     for element in firework0:
#       element.update()
#       element.display()
#       if element.done():
#         firework0.pop(firework0.index(element))
#     pygame.display.update()
#
#
#
# pygame.quit()
