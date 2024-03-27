import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from entity import Entity
import json
import object


class Map():
    def __init__(self,game_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.game_manager = game_manager
        self.tile_size = 60
        self.tiles = set()

        with open("map.json", "r") as f:
            self.map_data = json.load(f)

    def load(self):
        self.x, self.y = 0, 0

        for i, row in enumerate(self.map_data):
            for j, cell in enumerate(row):
                if cell == ' ': continue

                match cell:
                    case 'f': entity_name = 'block'
                    case 'l': entity_name = 'ladder'
                
                block_entity = Entity(
                    entity_name,
                    Vector(
                      self.tile_size * j + self.tile_size / 2,
                      self.tile_size * i + self.tile_size / 2
                    ),
                    img_url=self.get_tile_image(cell),
                    img_dest_dim=(60,60)
                )

                self.game_manager.add_entity(block_entity)

    def get_tile_image(self, char) -> str:
        match char:
            case 'f':
                return 'images/stone.png'
            case 'l':
                return 'images/ladder.png'

        return ' '
