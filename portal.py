from entity import Entity

class Portal(Entity):
    def __init__(self, name, direction=1, **kwargs) -> None:
        super().__init__(name, **kwargs)
        
        self.name = name
        self.direction = direction

        self.collision_mask = ['player', 'enemy', 'player_projectile', 'enemy_projectile']

    def update(self):
        if self.game_manager.interaction_manager.is_overlapping(self.game_manager.player, self):
            self.game_manager.map.change_room(self.direction)