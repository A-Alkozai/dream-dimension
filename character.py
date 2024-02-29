import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from entity import Entity

class Character(Entity):
    def __init__(self, floor_start, floor_border, **kwargs):
        super().__init__(**kwargs)

#floor_level = floor.start.y - floor.border - img_dest_dim[1]/2
        # overriding gravity-related variables
        self.gravity = True

        # variables to make image
        #self.img = simplegui._load_local_image("images/character_img.png")
        #self.img_dim = (self.img.get_width(), self.img.get_height())
        #self.img_centre = (self.img_dim[0]/2, self.img_dim[1]/2)
        #self.img_dest_dim = (100, 100)
        #self.img_pos = Vector(0, 0)
        #self.img_rotation = 0

        # ground level
        self.ground = floor_start.y - floor_border - self.img_dest_dim[1]/2

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
