from state import State


class Projectile(State):
    def __init__(self, name, damage=1, **kwargs):
        super().__init__(name, **kwargs)

        self.name = name
        self.GRAVITY = False
        self.IDLE = False
        self.DEAD = False

        self.collision_mask = ['ladder', 'player_projectile', 'player', 'enemy', 'enemy_projectile', 'portal']

        self.is_right = True
        self.is_red = True
        self.is_friendly = True
        self.damage = damage

        if name.startswith('player'):
            self.target_names = ['enemy', 'block', 'enemy_projectile']
        if name.startswith('enemy'):
            self.target_names = ['player', 'block', 'player_projectile']

    def update(self):
        self.set_direction(self.is_right)
        self.frame_update()
        self.movement()
        self.velocity.y = 0
        self.position.add(self.velocity)
        self.boundaries()
        self.velocity.multiply(0.85)

<<<<<<< HEAD
        #
        targets = [entity for entity in self.game_manager.all_entities if entity.name in self.target_names]
        for target in targets:
            if self.game_manager.interaction_manager.is_overlapping(self, target):
                # do damage to target
                target.damaged += self.damage
                self.DEAD = True
                break

        if self.DEAD:
            self.game_manager.remove_entity(self)
=======
        targets = [entity for entity in self.game_manager.all_entities if entity.name in self.targets_names]
        for target in targets:
            if self.game_manager.interaction_manager.is_overlapping(self, target):
                # do damage to target
                self.destroy()
                target.deal_damage(self.damage)
                
                # target.health -= self.damage
>>>>>>> 818937f2c5f104406acda261ffcd459a223d7bde

    def frame_update(self):
        # Choose correct row
        self.frame_index[1] = 1
        if self.is_red:
            self.frame_index[1] = 0

        if self.frame_count % 3 == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % 15
        self.frame_count += 1

    def set_direction(self, is_right):
        self.RIGHT = False
        self.LEFT = True
        self.rotation = 3
        if is_right:
            self.RIGHT = True
            self.LEFT = False
            self.rotation = 0

    def boundaries(self):
        if self.position.x <= 0 or self.position.x >= 1920 or self.position.y <= 0 or self.position.y >= 1080:
            self.DEAD = True
