from vector import Vector
from state import State
from entity import Entity


class Projectile(Entity):
    def __init__(self, speed=1.2, damage=1, **kwargs):
        self.img_url = 'images/magic_shot.png'
        self.column = 15
        self.row = 2
        self.img_dest_dim = (60, 60)
        super().__init__(img_url=self.img_url, column=self.column, row=self.row, img_dest_dim=self.img_dest_dim, **kwargs)

        self.state = State()
        self.state.GRAVITY = False
        self.collision_mask = ['ladder', 'player_projectile', 'player', 'enemy', 'enemy_projectile', 'portal']

        self.is_right = True
        self.is_red = True
        self.speed = speed
        self.damage = damage

        if self.kind.startswith('player'):
            self.target_kinds = ['enemy', 'block', 'enemy_projectile']
        if self.kind.startswith('enemy'):
            self.target_kinds = ['player', 'block', 'player_projectile']

    def update(self):
        self.set_direction(self.is_right)
        self.frame_update()
        self.movement()
        self.velocity.y = 0
        self.position.add(self.velocity)
        self.boundaries()
        self.velocity.multiply(0.85)

        targets = [entity for entity in self.game_manager.all_entities if entity.kind in self.target_kinds]
        for target in targets:
            if self.game_manager.interaction_manager.is_overlapping(self, target):
                # do damage to target
                self.destroy()
                target.deal_damage(self.damage)
            elif self.game_manager.interaction_manager.is_colliding(self, target)[0] and target.kind == 'block':
                self.destroy()

    def movement(self):
        # Move left/right
        if self.state.RIGHT:
            self.velocity += Vector(1, 0) * self.speed
        if self.state.LEFT:
            self.velocity += Vector(-1, 0) * self.speed

    def frame_update(self):
        # Choose correct row
        self.frame_index[1] = 1
        if self.is_red:
            self.frame_index[1] = 0

        if self.frame_count % 3 == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % 15
        self.frame_count += 1

    def set_direction(self, is_right):
        self.state.RIGHT = False
        self.state.LEFT = True
        self.rotation = 3
        if is_right:
            self.state.RIGHT = True
            self.state.LEFT = False
            self.rotation = 0

    def boundaries(self):
        if self.position.x <= 0 or self.position.x >= 1920 or self.position.y <= 0 or self.position.y >= 1080:
            self.die()

    def die(self):
        self.destroy()
