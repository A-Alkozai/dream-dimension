# Globals live in this class
from player import Player
from vector import Vector

from enemy import Enemy
from map import MapManager
from interaction import Interaction
from healthbar import HealthBar

class GameState:
    def __init__(self, frame, width, height) -> None:
        self.CANVAS_WIDTH = width
        self.CANVAS_HEIGHT = height

        self.frame = frame

        self.all_entities = []
        self.player = None
        self.player_health = 3

        self.healthbar = HealthBar()

        self.interaction_manager = Interaction()
        
        self.map = MapManager(self)
        self.map.load()

        # Create player
        # self.player = Player('player',walk_frames=8, jump_frames=2, attack_frames=4, dmg_frames=2, img_url="images/player.png",
        #                 img_dest_dim=(60, 60), position=Vector(500, 700), row=13, column=8, game_manager=self)

        # # Create enemies
        # self.enemy1 = Enemy('enemy', is_ranged=False, player=self.player, walk_frames=3, jump_frames=2, attack_frames=3,
        #             dmg_frames=2, speed=0.6, img_url="images/orc_warrior.png", img_dest_dim=(60, 60),
        #             position=Vector(100, 100), row=7, column=4, game_manager=self)
        # self.enemy2 = Enemy('enemy', is_ranged=True, player=self.player, walk_frames=3, jump_frames=2, attack_frames=4,
        #             dmg_frames=2, speed=0.4, img_url="images/orc_hunter.png", img_dest_dim=(60, 60),
        #             position=Vector(900, 100), row=7, column=8, game_manager=self)
        # self.enemy3 = Enemy('enemy', is_ranged=True, player=self.player, walk_frames=3, jump_frames=2, attack_frames=4,
        #             dmg_frames=2, speed=0.4, img_url="images/orc_shaman.png", img_dest_dim=(60, 60),
        #             position=Vector(1000, 100), row=7, column=8, game_manager=self)

        # self.all_entities.append(self.player)
        # self.all_entities.append(self.enemy1)
        # self.all_entities.append(self.enemy2)
        # self.all_entities.append(self.enemy3)
    
    def add_entity(self, entity):
        self.all_entities.append(entity)

    def remove_entity(self, entity):
        self.all_entities.remove(entity)

    def clear_screen(self):
        self.all_entities = []

    def draw(self, canvas):
        # for item in self.all_entities: print(item.name, end=' ')
        # print()

        self.healthbar.draw(canvas, self.player.health)

        for entity in self.all_entities:
            entity.update()
            entity.draw(canvas)
        if len(self.all_entities) > 0: self.interaction_manager.calculate_all_collisions(self.all_entities)