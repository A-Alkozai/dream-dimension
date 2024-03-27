from entity import Entity

class Portal(Entity):
    def __init__(self, direction=1) -> None:
        super().__init__()

        self.direction = direction

    def update(self):
        if self.game_manager.interaction_manager.is_overlapping(self.game_manager.player, self):
            self.game_manager