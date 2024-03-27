import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from state import State
from projectile import Projectile

class Player(State):
    def __init__(self,name, **kwargs):
        super().__init__(name, **kwargs)

        self.name = name
        self.collision_mask = ['ladder', 'player_projectile', 'enemy', 'enemy_projectile']
        # Lives & Score tracker
        self.points = 0
        self.lives = 3

        self.grounded = False
        self.on_ladder = False

    def update(self):
        super().update()

        ground_blocks = [entity for entity in self.game_manager.all_entities if entity.name == 'block']
        ladders = [entity for entity in self.game_manager.all_entities if entity.name == 'ladder']

        # if self.game_manager.interaction_manager.in_collision(self, ground_blocks):                
        #     # set player grounded variable
        #     self.grounded = True
        for block in ground_blocks:
            if self.game_manager.interaction_manager.is_colliding(self, block)[0]:
                self.grounded = True

        # # check if we are on top of a ladder
        # for ladder in ladders:
        #     if self.game_manager.interaction_manager.is_overlapping(self, ladder):
        #         self.on_ladder = True
        #         break
        #     else:
        #         self.CLIMB = False

        #         self.on_ladder = False
            

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
        
        if key == simplegui.KEY_MAP['w']:
            self.CLIMB = True

    def key_up(self, key):
        if key == simplegui.KEY_MAP["a"]:
            self.LEFT = False
        if key == simplegui.KEY_MAP["d"]:
            self.RIGHT = False

        if key == simplegui.KEY_MAP['w']:
            self.CLIMB = False
            self.on_ladder = False

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
                                         speed=1.2, collision_mask=['ladder', 'player_projectile', 'player', 'enemy', 'enemy_projectile'], game_manager=self.game_manager)
            self.projectile.is_right = move_right
            self.game_manager.add_entity(self.projectile)