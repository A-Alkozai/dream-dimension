import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from state import State
from projectile import Projectile
from healthbar import HealthBar

class Player(State):
    def __init__(self,name, **kwargs):
        super().__init__(name, walk_frames=8, jump_frames=2, attack_frames=4, dmg_frames=2, img_url="images/player.png",
                        img_dest_dim=(60, 60), row=13, column=8, **kwargs)

        self.name = name
        self.collision_mask = ['ladder', 'player_projectile', 'enemy', 'enemy_projectile', 'portal']
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

        # print(self.health)
         # def update(self):
        enemies = [entity for entity in self.game_manager.all_entities if entity.name == 'enemy']
        for enemy in enemies:
            if self.game_manager.interaction_manager.is_colliding(self, enemy)[0]:
                self.deal_damage(enemy.damage)
                self.game_manager.remove_entity(enemy)


    def die(self):
        super().die()
        self.game_manager.clear_screen()
        self.game_manager.welcome_screen.show_welcome_screen = True
        # END SCREEN

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
                                         speed=1.2, game_manager=self.game_manager)
            self.projectile.is_right = move_right
            self.game_manager.add_entity(self.projectile)