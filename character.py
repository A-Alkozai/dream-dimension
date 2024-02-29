import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from gravity_entity import GravityEntity

class Character(GravityEntity):
    def __init__(self, ground_level):
        super().__init__()

        # overriding gravity-related variables
        self.gravity = True

        # variables to make image
        self.img = simplegui._load_local_image("images/character_img.png")
        self.img_dim = (self.img.get_width(), self.img.get_height())
        self.img_centre = (self.img_dim[0]/2, self.img_dim[1]/2)
        self.img_dest_dim = (100, 100)
        self.img_pos = Vector(0, 0)
        self.img_rotation = 0

        # ground level
        self.ground = ground_level

        # velocity variable
        self.velocity = Vector(0, 0)

        # variables for key binds
        self.w = False
        self.a = False
        self.s = False
        self.d = False

    def draw(self, canvas):
        self.update()
        canvas.draw_image(self.img, self.img_centre,
                          self.img_dim, self.img_pos.get_p(),
                          self.img_dest_dim, self.img_rotation)

    def update(self):
        self.movement()
        self.img_pos.add(self.velocity)
        self.img_pos.y = min(self.img_pos.y, self.ground)
        self.velocity.multiply(0.85)

    def movement(self):
        if self.w:
            self.velocity += Vector(0, -15)
        if self.a:
            self.velocity += Vector(-2, 0)
        if self.s:
            pass
        if self.d:
            self.velocity += Vector(2, 0)

    def key_down(self, key):
        if key == simplegui.KEY_MAP["w"]:
            self.w = True
        if key == simplegui.KEY_MAP["a"]:
            self.a = True
        if key == simplegui.KEY_MAP["s"]:
            self.s = True
        if key == simplegui.KEY_MAP["d"]:
            self.d = True

    def key_up(self, key):
        if key == simplegui.KEY_MAP["w"]:
            self.w = False
        if key == simplegui.KEY_MAP["a"]:
            self.a = False
        if key == simplegui.KEY_MAP["s"]:
            self.s = False
        if key == simplegui.KEY_MAP["d"]:
            self.d = False
