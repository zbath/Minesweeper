import pygame
import random

class windisplay:

    """
    The windisplay class displays fireworks to the screen according to rows and colums
    that are given.
    """
    def __init__(self, board_size_x, board_size_y, display):

      """Constructor to initialize the winning screen of the game.
      :Param board_size_x: the rows of the gameboard.
      :Param board_size_y: the columns of the gameboard.
      :Param display, the running game screen.
      :return: None
      """

      #Set it to true to enable to while loop.
      self.run = True

      #225+width of the gameboard*35 is the actual width of the gameboard.
      self.board_size_x=225+board_size_x*35

      #5+board_size_y*35 is the actual height of the gameboard.
      self.board_size_y= max(5+board_size_y*35, 575)
      self.display=display

    #Method to generate the fireworks to the display screen.
    def displayfireworks(self):

        """
        Main body to display fireworks to the screen
        """

        #Creating the "You win!" sentence.
        font =pygame.font.SysFont('comicsans', 50, True)
        text= font.render("You win!", 1, (250, 250, 250))

        #Put the width and height of the screen into an array, nothing special.
        screen_size=[self.board_size_x, self.board_size_y]

        #Array to store the firework objects that are geneated.
        firework0 = []

        #Determine how fast is the fading of the screen, the last parameter for RGB is opacity, which in our case is 10
        BLACK_FADED = [0, 0, 0, 10]

        #The surface has per pixel transparency.
        blackSurf = pygame.Surface(screen_size).convert_alpha()
        blackSurf.fill(BLACK_FADED)

        while self.run:

            #Cover the origin screen with a black surface with opacity.
            self.display.blit(blackSurf, (0,0))

            #Check if the user tries to quit, if it's the case, then the loop break.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            #Generating fireworks in random rate
            if random.randint(0, 101) < 10:
              firework0.append(firework(self.board_size_x, self.board_size_y, self.display))

            self.display.blit(self.display, (0,0))

            #Keep displaying "You win!" to the screen.
            self.display.blit(text, (self.board_size_x/2-100, self.board_size_y/2))

            #Updating the status of the fireworks, and displaying them to the screen.
            #If a particular firework is done, it would get poped from the fireworks array
            for element in firework0:
              element.update()
              element.display()
              if element.done():
                firework0.pop(firework0.index(element))

            #Refreshing the screen
            pygame.display.update()

class particle:

        """
        The particle class hold all the attributes of a single firework particle.
        """
        #Class variable that won't change (When firework rising up, this how fast it will rise).
        gravity= 1


        def __init__(self, x, y, first, color_A, color_B, color_C, display):
         """
         Constructor to initialize a single firework particle.
         :Param: x: row coordinate of a particle.
         :Param: y: Colum coordinate of a particle.
         :Param: first: Determine if the particle is the exploder or not during construction time.
         :Param: color_A: Random values from 0-255 to put in the RGB when the firework being geneated.
         :Param: color_B: Random values from 0-255 to put in the RGB when the firework being geneated.
         :Param: color_C: Random values from 0-255 to put in the RGB when the firework being geneated.
         :Param: display: the running screen.
         """
              self.x=x
              self.y=y

              #How fast the particle change its velocity in both x and y directions.
              self.accel_x=0
              self.accel_y=0
              self.first=first

              #Determine how long the firework going to last after the first particle explodes.
              self.life=200
              self.color_A=color_A
              self.color_B=color_B
              self.color_C=color_C

              #Give ability to draw on the surface.
              self.window=display

              #If the particle is a exploder, all it does just to rise up, and this is why the x coordinate is not changing.
              if self.first:
               self.vel_x=0
               self.vel_y=random.randint(-30, -20)
              #Else the particle is given a random velocities for both x and y coordinates.
              else:
                  self.vel_x=random.randint(-30, 30)
                  self.vel_y=random.randint(-30, 30)

        def applyGravity(self):
        """
        Setting the acceleration in the y direction to Class varibale gravity.
        :return: none
        """
          self.accel_y =particle.gravity

        def update(self):
        """
        Updating every aspect of a single particle, changing its velocities in both x and y directions by adding them to x and y accelerations respectively, and its current position by adding velocities to x and y coordinates respectively.
        Setting acceleration in the y direction to 0 to make sure the particle won't go too fast in the y direction.
        :return: none
        """
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
            """
            Draw the particle to the screen.
            :return: none
            """
            if self.life > 0:
             pygame.draw.circle(self.window, (self.color_A, self.color_B, self.color_C), (self.x, self.y), 1)

        def done(self):
            """
            Determine whether the particle is done or not.
            :return: none
            """
            if self.life <= 0:
                return True
            else:
                return False

class firework:


     def __init__(self, board_size_x, board_size_y, display):
         """
         Constructor to initialize a firework.
         :Param board_size_x: number of rows of the gameboard
         :Param board_size_y: number of columns of the gameboard
         :Param display: the running screen
         """

       #Assign and initialize particle0 to be an exploder
       self.particle0=particle(random.randint(0, board_size_x), board_size_y-30, True, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), display)
       self.exploded=False
       self.particles=[]

     def createSubPar(self):
         """
         Create 100 particles with random velocities in both x and y directions, and being put in the particles array.
         :return: none
         """
       for element in range(0, 99):
         tempPar = particle(self.particle0.x, self.particle0.y, False, self.particle0.color_A, self.particle0.color_B, self.particle0.color_C, self.particle0.window)
         self.particles.append(tempPar)

     def update(self):
         """
         Updating and changing the current position of the particle, and if that particle is an exploder,
         when velocity in y direction reachs 0, it would creates an array of particles,
         and those particles have random velocities in both x and y direction.
         Else the particle is exploded, the method will simply update the status of each of the sub particles, and the particle will get poped from the array if it's done.
         :return: none
         """
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
         """
         Create 100 particles with random velocities in both x and y directions, and being put in the particles array.
         :return: none
         """
          self.createSubPar()

     def display(self):
         """
         If the particle hasn't exploded yet, the method would just update the changes of the exploder to the screen.
         Else the method would update each sub particles' changes to the screen
         :return: none
         """
       if not self.exploded:
        self.particle0.redraw()
       else:
           for element in self.particles:
             element.redraw()

     def done(self):
         """
         Check if the firework is done or not.
         The reason for this method is to make sure when the firework is done, it will get deleted to stablize the FPS.
         :return: none
         """
         if self.exploded and len(self.particles) == 0:
            return True
         else:
             return False
