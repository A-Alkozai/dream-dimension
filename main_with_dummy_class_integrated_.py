import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from gravity import Gravity
from character import Character
from floor import Floor
from dummy_character import DummyCharacter


def draw(canvas):
    gravity.gravity()
    for entity in all_entities:
        entity.draw(canvas)


# dimensions of canvas
canvas_width = 900
canvas_height = 700

# Floor creation
floor = Floor((0, canvas_height-101), (canvas_width-1, canvas_height-101), 100, "Grey")

# 1. loading image
img = simplegui._load_local_image("character_img.png")

# 2. making variables
img_dim = (img.get_width(), img.get_height())
img_centre = (img_dim[0]/2, img_dim[1]/2)
img_dest_dim = (100, 100)
img_pos = (canvas_width/2, floor.start.y-floor.border-img_dest_dim[1]/2)
img_rot = 0

# 3. creating character
character = Character(img, img_centre, img_dim,
                      img_pos, img_dest_dim, img_rot)


# creation of canvas
frame = simplegui.create_frame("Stick man", canvas_width, canvas_height)
frame.set_canvas_background("White")

# setting handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(character.key_down)
frame.set_keyup_handler(character.key_up)

# 4. creating dummy character
dummy_character = DummyCharacter(floor, frame, canvas_width)

# list of all entities
all_entities = [character, floor, dummy_character]

# Gravity creation
gravity = Gravity(all_entities)



# starting frame
frame.start()
