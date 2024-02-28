import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from gravity_entity import GravityEntity

class DummyCharacter(GravityEntity):
  def __init__(self, floor, frame, canvas_width):
      super().__init__()

      # overriding gravity-related variables
      self.gravity = False  # Gravity is not applied to the dummy character

      # reference to the floor
      self.floor = floor

      # reference to the frame
      self.frame = frame

      # canvas width
      self.canvas_width = canvas_width

      # variables to make image
      self.img = simplegui._load_local_image("dummy_character.png")
      self.img_centre = (self.img.get_width() / 2, self.img.get_height() / 2)
      self.img_dim = (self.img.get_width(), self.img.get_height())
      self.img_dest_dim = (100, 100)
      self.img_rotation = 0

      # initial position
      self.img_pos = Vector(20, (self.floor.start.y-50) - self.img_dest_dim[1])

      # velocity variable
      self.velocity = Vector(2, 0)  # Initial velocity for moving right

  def draw(self, canvas):
      self.update()
      canvas.draw_image(self.img, self.img_centre,
                        self.img_dim, self.img_pos.get_p(),
                        self.img_dest_dim, self.img_rotation)

  def update(self):
      self.move()

      # ensure the dummy stays within the bounds of the floor
      self.img_pos.x = max(self.img_pos.x, self.floor.start.x + self.img_dest_dim[0] / 2)
      self.img_pos.x = min(self.img_pos.x, self.floor.end.x - self.img_dest_dim[0] / 2)

  def move(self):
      # Move the dummy character horizontally across the canvas
      self.img_pos.x += self.velocity.x

      # If the dummy character reaches the right edge, reverse direction
      if self.img_pos.x + self.img_dest_dim[0] / 2 >= self.canvas_width:
          self.velocity.x = -abs(self.velocity.x)

      # If the dummy character reaches the left edge, reverse direction
      elif self.img_pos.x - self.img_dest_dim[0] / 2 <= 0:
          self.velocity.x = abs(self.velocity.x)
















