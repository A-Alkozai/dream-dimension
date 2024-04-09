from entity import Entity
from vector import Vector
import math


class Effect(Entity):
    def __init__(self, name, position, game_manager, **kwargs):

        if name == 'blood':
            self.img_url = 'images/sprites/effects/blood.png'
            self.column = 6
            self.row = 5
            self.img_dest_dim = (80, 80)
            self.total_frames = 30
            self.frame_speed = 2
        elif name == 'player_explosion' or name == 'enemy_explosion':
            self.img_url = 'images/sprites/effects/explosion.png'
            self.column = 29
            self.row = 1
            self.img_dest_dim = (400, 400)
            self.total_frames = 28
            self.frame_speed = 5
        elif name == 'fire_spiral':
            self.img_url = 'images/sprites/effects/fire_spiral.png'
            self.column = 9
            self.row = 1
            self.img_dest_dim = (70, 70)
            self.total_frames = 8
            self.frame_speed = 6
        elif name == 'water_spiral':
            self.img_url = 'images/sprites/effects/water_spiral.png'
            self.column = 9
            self.row = 1
            self.img_dest_dim = (70, 70)
            self.total_frames = 8
            self.frame_speed = 6
        elif name == 'impact':
            self.img_url = 'images/sprites/effects/impact.png'
            self.column = 4
            self.row = 1
            self.img_dest_dim = (140, 100)
            self.total_frames = 3
            self.frame_speed = 10

        super().__init__(kind='sfx', name=name, img_url=self.img_url, column=self.column, row=self.row,
                         position=position, game_manager=game_manager, img_dest_dim=self.img_dest_dim, **kwargs)
        self.frame_number = 0

    def draw(self, canvas):
        super().draw(canvas)
        self.update()

    def update(self):
        if self.frame_count == 10:
            self.damage_parameter()
        if self.frame_count % self.frame_speed == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % self.column
            if self.frame_index[0] == 0:
                self.frame_index[1] = (self.frame_index[1] + 1) % self.row
            self.frame_number += 1

        if self.frame_number == self.total_frames:
            self.game_manager.remove_entity(self)
        self.frame_count += 1

    def damage_parameter(self):
        radius = 150
        target_kind = []
        if self.name == 'player_explosion':
            target_kind = ['enemy']
            dmg = 1
        elif self.name == 'enemy_explosion':
            target_kind = ['player']
            dmg = 2
        targets = [entity for entity in self.game_manager.all_entities if entity.kind in target_kind]
        for target in targets:
            position = Vector(self.position.x, self.position.y)
            distance = math.sqrt((position.x - target.position.x) ** 2 + (position.y - target.position.y) ** 2)
            if distance <= radius:
                target.deal_damage(dmg)
