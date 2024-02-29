# TEMP COMMENT: This class will have variables accessible to all entities.
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector

class Entity:
    def __init__(self, 
                 position=Vector(), 
                 velocity=Vector(), 
                 rotation=0, 
                 img_url="", 
                 img_dest_dim=None,
                 gravity_strength=2, 
                 gravity_toggle=False):

        self.position = position
        self.velocity = velocity
        self.rotation = rotation

        self.img_url = img_url

        if img_url is None: self.img = simplegui._load_local_image("images/placeholder.jpg")
        else: self.img = simplegui._load_local_image(self.img_url)

        self.img_centre = (self.img.get_width() / 2, self.img.get_height() / 2)
        self.img_dim = (self.img.get_width(), self.img.get_height())
        self.img_dest_dim = self.img_dim if img_dest_dim is None else img_dest_dim

        self.weight = gravity_strength
        # perhaps change the name to is_affected_by_gravity ?
        self.gravity = gravity_toggle
        
    def load_image(self):
        pass

    def draw(self, canvas):
        pass
    def update(self): pass
