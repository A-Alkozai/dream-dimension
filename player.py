import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from state import State

class Player(State):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.ground = floor.start.y - floor.border - self.img_dest_dim[1]/2

        # variables for key binds
        # self.w = False
        # self.a = False
        # self.s = False
        # self.d = False

    def state_update(self):
        pass

    def key_down(self, key):
        if key == simplegui.KEY_MAP["w"]: self.JUMP = True
        if key == simplegui.KEY_MAP["a"]: self.LEFT = True
        if key == simplegui.KEY_MAP["d"]: self.RIGHT = True
        if key == simplegui.KEY_MAP["f"]: self.ATTACK = True
        if key == simplegui.KEY_MAP["c"]: self.DAMAGE = True

    def key_up(self, key):
        if key == simplegui.KEY_MAP["w"]: self.JUMP = False
        if key == simplegui.KEY_MAP["a"]: self.LEFT = False
        if key == simplegui.KEY_MAP["d"]: self.RIGHT = False
        # if key == simplegui.KEY_MAP["f"]: self.ATTACK = False
