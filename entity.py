import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector


class Entity:
    def __init__(self,
                 name='',
                 position=Vector(),
                 velocity=Vector(),
                 rotation=0,
                 img_url="",
                 img_dest_dim=None,
                 row=1,
                 column=1,
                 frames=1,
                 game_manager=None,
                 collision_mask=[],
                 health=6
                 ):

        self.game_manager = game_manager
        self.name = name
        self.collision_mask = collision_mask

        self.active = True

        self.position = position
        self.velocity = velocity
        self.rotation = rotation

        self.health = health

        self.img_url = img_url

        if img_url is None:
            self.img = simplegui._load_local_image("images/placeholder.jpg")
        else:
            self.img = simplegui._load_local_image(img_url)

        self.img_dim = (self.img.get_width(), self.img.get_height())
        self.img_dest_dim = self.img_dim if img_dest_dim is None else img_dest_dim

        self.row = row
        self.column = column
        self.totalFrames = frames
        self.frame_count = 0
        self.frame_width = self.img.get_width() / column
        self.frame_height = self.img.get_height() / row
        self.img_dim = (self.frame_width, self.frame_height)

        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
        self.frame_index = [0, 0]

    def __str__(self):
        return self.name

    def destroy(self):
        try:
            self.game_manager.remove_entity(self)
        except:
            pass

    def draw(self, canvas):
        if not self.active: return

        frame_centre = (self.frame_width * self.frame_index[0] + self.frame_centre_x,
                        self.frame_height * self.frame_index[1] + self.frame_centre_y)

        canvas.draw_image(self.img,
                          frame_centre,
                          self.img_dim,
                          self.position.get_p(),
                          self.img_dest_dim,
                          self.rotation)

    def update(self):
        self.frame_index[0] = (self.frame_index[0] + 1) % self.column
        if self.frame_index[0] == 0:
            self.frame_index[1] = (self.frame_index[1] + 1) % self.row

    def on_collision(self, collider):
        pass

    def deal_damage(self, dmg):
        pass