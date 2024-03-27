import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from state import State
from projectile import Projectile


class Player(State):
    def __init__(self,name, **kwargs):
        super().__init__(name, **kwargs)

        self.name = name
        self.collision_mask = ['ladder']
        # Lives & Score tracker
        self.points = 0
        self.lives = 3
        self.grounded = False
        self.on_ladder = False


    def key_down(self, key):
        if key == simplegui.KEY_MAP["space"] and self.grounded:
            self.JUMP = True
            # self.grounded = False
        if key == simplegui.KEY_MAP["a"]:
            self.LEFT = True
        if key == simplegui.KEY_MAP["d"]:
            self.RIGHT = True
        if key == simplegui.KEY_MAP["f"]:
            self.ATTACK1 = True
        if key == simplegui.KEY_MAP["q"]:
            self.ATTACK2 = True
        if key == simplegui.KEY_MAP["c"]:
            self.HURT = True
        
        if key == simplegui.KEY_MAP['w'] and self.on_ladder:
            self.CLIMBING = True

    def key_up(self, key):
        if key == simplegui.KEY_MAP["a"]:
            self.LEFT = False
        if key == simplegui.KEY_MAP["d"]:
            self.RIGHT = False

        if key == simplegui.KEY_MAP['w']:
            self.CLIMBING = False

    def shoot(self):
        if self.mana >= 40:
            self.mana -= 40
            self.start_mana_recharge()

            move_right = True
            adjust_x = 10
            if self.frame_index[1] == 10:
                move_right = False
                adjust_x = -10
            self.projectile = Projectile('player_projectile', img_url="images/magic_shot.png", img_dest_dim=(60, 60),
                                         position=Vector(self.position.x + adjust_x, self.position.y), row=2, column=15,
                                         speed=1.2)
            self.projectile.is_right = move_right
            self.game_manager.add_entity(self.projectile)