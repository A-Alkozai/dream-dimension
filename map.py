import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from entity import Entity
from portal import Portal
from player import Player
from enemy import Enemy
import json
import random

class MapManager():
    def __init__(self,game_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.game_manager = game_manager
        self.tile_size = 60
        self.tiles = set()

        self.current_room_index = 0

        with open("map.json", "r") as f:
            self.map_data = json.load(f)

    def change_room(self, direction):
        self.current_room_index += direction
        self.game_manager.all_entities = []

        # save player health
        self.game_manager.player_health = self.game_manager.player.health
        self.load()

        self.game_manager.player.health = self.game_manager.player_health

    def load(self):
        self.x, self.y = 0, 0

        for i, row in enumerate(self.map_data[self.current_room_index]):
            for j, cell in enumerate(row):
                if cell == ' ': continue

                cell_pos = Vector(
                    self.tile_size * j + self.tile_size / 2,
                    self.tile_size * i + self.tile_size / 2
                )
                cell_image = self.get_tile_image(cell)

                match cell:
                    case 'f':
                        entity_name = 'block'
                        block_entity = Entity(entity_name, position=cell_pos, img_url=cell_image, img_dest_dim=(60,60))
                    case 'l': 
                        entity_name = 'ladder'
                        block_entity = Entity(entity_name, position=cell_pos, img_url=cell_image, img_dest_dim=(60,60))
                    case 'p':
                        entity_name = 'portal'
                        block_entity = Portal(entity_name, position=cell_pos, img_url=cell_image, img_dest_dim=(60,60), game_manager=self.game_manager)
                    case 'p-':
                        entity_name = 'portal'
                        block_entity = Portal(entity_name, position=cell_pos, direction=-1, img_url=cell_image, img_dest_dim=(60,60), game_manager=self.game_manager)
                    case 's':
                        entity_name = 'player'
                        block_entity = Player(entity_name,position=cell_pos, game_manager=self.game_manager, health=self.game_manager.player_health)

                        # input handling for player
                        self.game_manager.frame.set_keydown_handler(block_entity.key_down)
                        self.game_manager.frame.set_keyup_handler(block_entity.key_up)

                        self.game_manager.player = block_entity
                        self.game_manager.player_health = block_entity.health
                    case 'e':
                        entity_name = 'enemy'
                        enemies = [
                            Enemy('enemy', is_ranged=False,
                                walk_frames=3, jump_frames=2, attack_frames=3,
                                dmg_frames=2, speed=0.6, img_url="images/orc_warrior.png",
                                img_dest_dim=(60, 60),position=cell_pos, row=7,
                                column=4, game_manager=self.game_manager, health_max=2),
                            Enemy('enemy', is_ranged=True,
                                walk_frames=3, jump_frames=2, attack_frames=4,
                                dmg_frames=2, speed=0.4, img_url="images/orc_hunter.png",
                                img_dest_dim=(60, 60), position=cell_pos, row=7,
                                column=8, game_manager=self.game_manager, health_max=2), 
                            Enemy('enemy', is_ranged=True,
                                walk_frames=3, jump_frames=2, attack_frames=4,
                                dmg_frames=2, speed=0.4, img_url="images/orc_shaman.png",
                                img_dest_dim=(60, 60),position=cell_pos, row=7,
                                column=8, game_manager=self.game_manager, health_max=2)
                        ]

                        block_entity = random.choice(enemies)                
                self.game_manager.add_entity(block_entity)

    def get_tile_image(self, char) -> str:
        match char:
            case 'f': return 'images/stone.png'
            case 'l': return 'images/ladder.png'
            case 'p' | 'p-': return 'images/door.png'

        return ' '
