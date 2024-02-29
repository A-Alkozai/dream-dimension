import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from entity import Entity

class Enemy(Entity):
    def __init__(self, floor, canvas_width, **kwargs):
        super().__init__(**kwargs)

        self.gravity = False  # Gravity is not applied to the dummy character

        self.floor = floor
        self.canvas_width = canvas_width

        #self.img = simplegui._load_local_image("images/npc.png")

        self.position = Vector(20, (self.floor.start.y-50) - self.img_dest_dim[1])
        self.velocity = Vector(2, 0)  # Initial velocity for moving right

    def draw(self, canvas):
        self.update()
        canvas.draw_image(self.img,
                          self.img_centre,
                          self.img_dim,
                          self.position.get_p(),
                          self.img_dest_dim,
                          self.rotation)

    def update(self):
        self.move()

        # ensure the enemy stays within the bounds of the floor
        self.position.x = max(self.position.x, self.floor.start.x + self.img_dest_dim[0] / 2)
        self.position.x = min(self.position.x, self.floor.end.x - self.img_dest_dim[0] / 2)

    def move(self):
        # Move the enemy character horizontally across the canvas
        self.position.x += self.velocity.x

        # If the enemy haracter reaches the right edge, reverse direction
        if self.position.x + self.img_dest_dim[0] / 2 >= self.canvas_width:
            self.velocity.x = -abs(self.velocity.x)

        # If the enemy character reaches the left edge, reverse direction
        elif self.position.x - self.img_dest_dim[0] / 2 <= 0:
            self.velocity.x = abs(self.velocity.x)
