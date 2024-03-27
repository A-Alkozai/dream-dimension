import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from entity import Entity
import json


class Map():
    def __init__(self,welcome_screen, **kwargs):
        super().__init__(**kwargs)
        self.welcome_screen = welcome_screen
        self.tile_size = 60
        self.tiles = set()

        with open("map.json", "r") as f:
            self.map_data = json.load(f)

    def draw(self, canvas: simplegui.Canvas):
        self.x, self.y = 0, 0

        # draw grid
        for i in range(1920):
            if i % 60 == 0:
                canvas.draw_line((i, 0), (i, 1920), 2, 'black')
        for i in range(1080):
            if i % 60 == 0:
                canvas.draw_line((0, i), (1080, i), 2, 'black')

        for i, row in enumerate(self.map_data):
            for j, column in enumerate(row):

                tile_image = simplegui._load_local_image(self.get_map_tile(column))

                # calculate tile centre
                tile_pos = (
                    self.tile_size * j + self.tile_size / 2,
                    self.tile_size * i + self.tile_size / 2
                )
                # add tile position to set
                if column != '':
                    self.tiles.add(tile_pos)

                canvas.draw_image(tile_image, (8,8), (16,16), tile_pos, (self.tile_size, self.tile_size))

    def get_map_tile(self, char) -> str:
        match char:
            case 'f':
                return 'images/stone.png'

        return ''
