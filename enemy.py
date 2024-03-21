import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from player import Player
from vector import Vector
from state import State
import math
import random

class Enemy(State):
    def __init__(self, range, canvas_width, mana_max=150, mana_recharge_rate=2, **kwargs):
        super().__init__(**kwargs)

        self.range = range
        self.position = kwargs.get('position', None)
        if self.position is None:
            # If position is not provided, randomly select a position within a range
            self.position = Vector(random.randint(100, 1500), random.randint(100, 800))
        self.velocity = Vector(0, 0)
        self.canvas_width = canvas_width
        self.move_right = True
        self.move_distance = 100
        self.current_distance = 0

        # Mana attributes for enemy
        self.max_mana = mana_max
        self.current_mana = self.max_mana
        self.mana_recharge_rate = mana_recharge_rate
        self.mana_recharge_timer = simplegui.create_timer(1000, self.recharge_mana)

    def state_update(self):
        distance_to_player = math.sqrt((self.player.position.x - self.position.x) ** 2 + (self.player.position.y - self.position.y) ** 2)

        tracking_range = 200
        attack_range = 100

        if distance_to_player < tracking_range:
            self.track_player()
        else:
            self.move_back_and_forth()

        if self.range:
            if distance_to_player < attack_range:
                self.ATTACK = True

                if self.player.position.x > self.position.x:
                    self.RIGHT = True
                    self.LEFT = False
                else:
                    self.LEFT = True
                    self.RIGHT = False
            else:
                self.ATTACK = False
        else:
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
        self.speed = 0.5

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

    def start_mana_recharge(self):
        self.mana_recharge_timer.start()

    def stop_mana_recharge(self):
        self.mana_recharge_timer.stop()

    def recharge_mana(self):
        self.current_mana = min(self.current_mana + self.mana_recharge_rate, self.max_mana)
