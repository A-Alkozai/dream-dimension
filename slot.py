from entity import Entity
from vector import Vector


class Slot(Entity):
    def __init__(self, game_manager):
        self.position = Vector(55, 60)
        self.img_url = 'images/slots.png'
        super().__init__(kind='display', name='slots', position=self.position, img_url=self.img_url,
                         img_dest_dim=(100, 100), game_manager=game_manager, column=5)

    def update(self):
        # Access player state
        state = self.game_manager.player.state

        # Check which projectiles have been unlocked
        unlocked1 = self.game_manager.player.shotRed
        unlocked2 = self.game_manager.player.shotPurple
        unlocked3 = self.game_manager.player.shotSpecial
        unlocked4 = self.game_manager.player.shotSpecial2

        # Update to correct slot image
        if state.SLOT1 and unlocked1:
            self.frame_index[0] = 1
        elif state.SLOT2 and unlocked2:
            self.frame_index[0] = 2
        elif state.SLOT3 and unlocked3:
            self.frame_index[0] = 3
        elif state.SLOT4 and unlocked4:
            self.frame_index[0] = 4
        else:
            self.frame_index[0] = 0
