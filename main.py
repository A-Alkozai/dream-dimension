import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from gravity import Gravity
from character import Character
from floor import Floor


def draw(canvas):
    gravity.gravity()
    for entity in all_entities:
        entity.draw(canvas)


# dimensions of canvas
canvas_width = 900
canvas_height = 700

# Floor creation
floor = Floor((0, canvas_height-101), (canvas_width-1, canvas_height-101), 100, "Grey")

# Character creation

# 1. loading image
img = simplegui.load_image("/Users/ahadalkozai/Downloads/5a4bc99c2da5ad73df7efe66.png")

# 2. making variables
img_dim = (img.get_width(), img.get_height())
img_centre = (img_dim[0]/2, img_dim[1]/2)
img_dest_dim = (100, 100)
img_pos = (canvas_width/2, floor.start.y-floor.border-img_dest_dim[1]/2)
img_rot = 0

# 3. creating character
character = Character(img, img_centre, img_dim,
                      img_pos, img_dest_dim, img_rot)

# list of all entities
all_entities = [character, floor]

# Gravity creation
gravity = Gravity(all_entities)

# creation of canvas
frame = simplegui.create_frame("Stick man", canvas_width, canvas_height)
frame.set_canvas_background("White")

# setting handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(character.key_down)
frame.set_keyup_handler(character.key_up)

# starting frame
frame.start()
