import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from entity import Entity
from gravity import Gravity
from character import Character
from floor import Floor
from enemy import Enemy
from gun import Gun

# dimensions of canvas
canvas_width = 900
canvas_height = 700

floor = Floor((0, canvas_height-101), (canvas_width-1, canvas_height-101), 100, "Grey")

# creating character
character = Character(floor.start, floor.border, img_url="images/character_img.png", img_dest_dim=(100,100))

enemy = Enemy(floor, canvas_width, img_dest_dim=(100,100))

pistol = Gun()

all_entities = [character, floor, enemy, pistol]

gravity = Gravity(all_entities)

# creation of canvas
frame = simplegui.create_frame("Stick man", canvas_width, canvas_height)
frame.set_canvas_background("White")

def draw(canvas):
    gravity.gravity()
    for entity in all_entities:
        entity.draw(canvas)

# setting handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(character.key_down)
frame.set_keyup_handler(character.key_up)

frame.set_mousedrag_handler(pistol.point_to_mouse)

# starting frame
frame.start()
