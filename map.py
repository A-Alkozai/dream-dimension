import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from entity import Entity
from portal import Portal
import json
import object


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
                        block_entity = Entity(entity_name, cell_pos,img_url=cell_image,img_dest_dim=(60,60))
                    case 'l': 
                        entity_name = 'ladder'
                        block_entity = Entity(entity_name, cell_pos,img_url=cell_image,img_dest_dim=(60,60))
                    # case 'p':
                    #     entity_name = 'ladder'
                    #     block_entity = Portal(entity_name, cell_pos,img_url=cell_image,img_dest_dim=(60,60))

                

                self.game_manager.add_entity(block_entity)

    def get_tile_image(self, char) -> str:
        match char:
            case 'f': return 'images/stone.png'
            case 'l': return 'images/ladder.png'
            case 'p': return 'images/door.png'

        return ' '
