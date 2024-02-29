# TEMP COMMENT: This class will have variables accessible to all entities.
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector

class Entity:
    def __init__(self, 
                 position=Vector(), 
                 velocity=Vector(), 
                 rotation=0, 
                 img_url="images/placeholder.png", 
                 img_dest_dim=None,
                 gravity_strength=2, 
                 gravity_toggle=False):

        self.position = position
        self.velocity = velocity
        self.rotation = rotation

        self.img = simplegui._load_local_image(img_url)
        self.img_centre = (self.img.get_width() / 2, self.img.get_height() / 2)
        self.img_dim = (self.img.get_width(), self.img.get_height())
        self.img_dest_dim = self.img_dim if img_dest_dim is None else img_dest_dim

        self.weight = gravity_strength
        # perhaps change the name to is_affected_by_gravity ?
        self.gravity = gravity_toggle
        
    def draw(self, canvas):
        pass
    def update(self): pass
