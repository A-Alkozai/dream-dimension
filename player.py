import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from state import State

class Player(State):
    def __init__(self, mana_max=100, mana_recharge_rate=1, **kwargs):
        super().__init__(**kwargs)
        self.points = 0
        self.lives = 3
        self.mana_max = mana_max
        self.mana_current = mana_max
        self.mana_recharge_rate = mana_recharge_rate
        self.mana_recharge_timer = simplegui.create_timer(1000, self.recharge_mana)

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

    def start_mana_recharge(self):
        self.mana_recharge_timer.start()

    def stop_mana_recharge(self):
        self.mana_recharge_timer.stop()

    def recharge_mana(self):
        self.mana_current = min(self.mana_current + self.mana_recharge_rate, self.mana_max)
