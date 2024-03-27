import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from projectile import Projectile
from vector import Vector
from state import State
import math


class Enemy(State):
    def __init__(self, is_ranged=True, mana_max=40, mana_recharge_rate=20, **kwargs):
        super().__init__(**kwargs)

        # create tracking and attack distance
        self.is_ranged = is_ranged
        if self.is_ranged:
            self.tracking_range = 400
            self.attack_range = 300
            self.fps = 16
        else:
            self.tracking_range = 400
            self.attack_range = 30
            self.fps = 6

        # Mana attributes for enemy
        self.max_mana = mana_max
        self.current_mana = self.max_mana
        self.mana_recharge_rate = mana_recharge_rate
        self.mana_recharge_timer = simplegui.create_timer(1000, self.recharge_mana)

    def state_update(self):
        super().state_update()

        # shortest distance
        distance_to_player = math.sqrt((self.player.position.x - self.position.x) ** 2
                                       + (self.player.position.y - self.position.y) ** 2)

        # If enemy close to player, attack player
        if distance_to_player < self.attack_range:
            self.ATTACK1 = True
            self.PATROL = False
            self.idle_frame = [0, 0]
            if self.player.position.x < self.position.x:
                self.idle_frame = [2, 0]

        # If enemy is far from player, move towards player position
        elif self.player.position.x - 25 > self.position.x and distance_to_player <= self.tracking_range:
            self.RIGHT = True
            self.LEFT = False
            self.PATROL = False
        elif self.player.position.x + 25 < self.position.x and distance_to_player <= self.tracking_range:
            self.LEFT = True
            self.RIGHT = False
            self.PATROL = False

        # Enemy patrol state
        else:
            self.PATROL = True

    def shoot(self):
        if self.is_ranged and self.mana >= 40:
            self.mana -= 40
            self.start_mana_recharge()

            move_right = True
            adjust_x = 10
            if self.frame_index[1] == 6:
                move_right = False
                adjust_x = -10
            self.projectile = Projectile(img_url="images/magic_shot.png", img_dest_dim=(50, 50),
                                         position=Vector(self.position.x + adjust_x, self.position.y), row=2, column=15,
                                         speed=1.2)
            self.projectile.is_red = False
            self.projectile.is_friendly = False
            self.projectile.is_right = move_right
