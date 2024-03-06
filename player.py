import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from entity import Entity


class Character(Entity):
    def __init__(self, floor, **kwargs):
        super().__init__(**kwargs)

        self.gravity = True

        self.ground = floor.start.y - floor.border - self.img_dest_dim[1]/2

        # variables for key binds
        self.w = False
        self.a = False
        self.s = False
        self.d = False

    def draw(self, canvas):
        self.update()
        canvas.draw_image(self.img, 
                          self.img_centre,
                          self.img_dim, 
                          self.position.get_p(),
                          self.img_dest_dim, 
                          self.rotation)

    def update(self):
        self.movement()
        self.position.add(self.velocity)
        self.position.y = min(self.position.y, self.ground)
        self.velocity.multiply(0.85)

    def movement(self):
        if self.w: self.velocity += Vector(0, -15)
        if self.a: self.velocity += Vector(-2, 0)
        if self.s: pass
        if self.d: self.velocity += Vector(2, 0)

    def key_down(self, key):
        if key == simplegui.KEY_MAP["w"]: self.w = True
        if key == simplegui.KEY_MAP["a"]: self.a = True
        if key == simplegui.KEY_MAP["s"]: self.s = True
        if key == simplegui.KEY_MAP["d"]: self.d = True

    def key_up(self, key):
        if key == simplegui.KEY_MAP["w"]: self.w = False
        if key == simplegui.KEY_MAP["a"]: self.a = False
        if key == simplegui.KEY_MAP["s"]: self.s = False
        if key == simplegui.KEY_MAP["d"]: self.d = False
