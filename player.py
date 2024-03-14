import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from state import State


class Player(State):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def state_update(self):
        pass

    def key_down(self, key):
        if key == simplegui.KEY_MAP["w"]: self.JUMP = True
        if key == simplegui.KEY_MAP["a"]: self.LEFT = True
        if key == simplegui.KEY_MAP["d"]: self.RIGHT = True
        if key == simplegui.KEY_MAP["f"]: self.ATTACK = True
        if key == simplegui.KEY_MAP["c"]: self.DAMAGE = True

    def key_up(self, key):
        if key == simplegui.KEY_MAP["a"]: self.LEFT = False
        if key == simplegui.KEY_MAP["d"]: self.RIGHT = False
