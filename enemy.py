import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from player import Player
from vector import Vector
from state import State


class Enemy(State):
    def __init__(self, position=Vector(50, 600), **kwargs):
        super().__init__(**kwargs)

        self.position = position
        self.velocity = Vector(0, 0)

