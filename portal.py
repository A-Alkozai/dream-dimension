from entity import Entity


class Portal(Entity):
    def __init__(self, direction=1, **kwargs) -> None:
        super().__init__(**kwargs)

        self.direction = direction
        self.collision_mask = ['player', 'enemy', 'player_projectile', 'enemy_projectile', 'sfx', 'drop']

    def update(self):
        if self.frame_count % 10 == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % self.column
            if self.frame_index[0] == 0:
                self.frame_index[1] = (self.frame_index[1] + 1) % self.row
        if self.game_manager.interaction_manager.is_overlapping(self.game_manager.player, self):
            self.game_manager.map.change_room(self.direction)
        self.frame_count += 1
