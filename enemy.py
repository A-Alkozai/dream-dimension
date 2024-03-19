import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from player import Player
from vector import Vector
from state import State


import math 

class Enemy(State):
    def __init__(self, canvas_width, welcome_screen, **kwargs):
        super().__init__(welcome_screen,**kwargs)
        self.welcome_screen = welcome_screen

        self.position = Vector(50, 600)
        self.velocity = Vector(0, 0)
        self.canvas_width = canvas_width
    def movement(self):
        if self.JUMP:
            self.velocity += Vector(0, -5) * self.speed
        elif self.GRAVITY:
            self.velocity.y += self.weight

        # Check if the enemy is at the boundary
        if self.position.x >= self.canvas_width:
            self.RIGHT = False
            self.LEFT = True
        elif self.position.x <= 0:  
            self.RIGHT = True
            self.LEFT = False

        # Update velocity and idle frame based on direction
        if self.LEFT:
            self.velocity += Vector(-1, 0) * self.speed
            self.idle_frame = [2, 0]
        elif self.RIGHT:
            self.velocity += Vector(1, 0) * self.speed
            self.idle_frame = [0, 0]

        # Update position
        self.position += self.velocity



    def state_update(self):

        distance_to_player = math.sqrt((self.player.position.x - self.position.x) ** 2 + (self.player.position.y - self.position.y) ** 2)

        tracking_range = 200

        if distance_to_player < tracking_range:
                self.track_player()

        else:
             self.move_horizontally()

        if abs(self.player.position.x - self.position.x)<25 and self.player.position.y > 800:
            self.ATTACK = True
        else:
            self.ATTACK = False

    def track_player(self):
        if self.player.position.x > self.position.x:
            self.RIGHT = True
            self.LEFT = False
        else:
            self.LEFT = True
            self.RIGHT = False

        self.speed = 0.3

    def move_horizontally(self):
         self.RIGHT = True
         self.LEFT = False
         self.speed = 0.2

#def movement(self):
 #   if self.JUMP:
  #      self.velocity += Vector(0, -5) * self.speed
   # elif self.GRAVITY:
    #    self.velocity.y += self.weight

    # Check if not at the boundary before updating velocity
#    if not (self.position.x >= self.canvas_width or self.position.x <= 0):
 #       if self.RIGHT:
  #          self.velocity += Vector(1, 0) * self.speed
   #         self.idle_frame = [0, 0]
    #    elif self.LEFT:
     #       self.velocity += Vector(-1, 0) * self.speed
      #      self.idle_frame = [2, 0]

    # Update position based on velocity
    #self.position += self.velocity