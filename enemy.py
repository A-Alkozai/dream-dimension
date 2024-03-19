import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from player import Player
from vector import Vector
from state import State
import math 
import random

class Enemy(State):
    def __init__(self, canvas_width, welcome_screen, **kwargs):
        super().__init__(welcome_screen,**kwargs)

        self.welcome_screen = welcome_screen
        self.position = kwargs.get('position', None)
        if self.position is None:
            # If position is not provided, randomly select a position within a range
            self.position = Vector(random.randint(100, 1500), random.randint(100, 800))
        self.velocity = Vector(0, 0)
        self.canvas_width = canvas_width
        self.move_right = True
        self.move_distance = 100
        self.current_distance = 0

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
             self.move_back_and_forth()

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

    def move_back_and_forth(self):
        if self.move_right:
            self.RIGHT = True
            self.LEFT = False
            self.current_distance += abs(self.velocity.x)  # Update current distance moved
            if self.current_distance >= self.move_distance:
                self.move_right = False  # Change direction when reached move distance
                self.current_distance = 0  # Reset current distance
        else:
            self.RIGHT = False
            self.LEFT = True
            self.current_distance += abs(self.velocity.x)  # Update current distance moved
            if self.current_distance >= self.move_distance:
                self.move_right = True  # Change direction when reached move distance
                self.current_distance = 0  # Reset current distance
        self.speed = 0.2

