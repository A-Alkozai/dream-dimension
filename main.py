import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entity import Entity
from gravity import Gravity
from player import Player
from floor import Floor
from enemy import Enemy
from vector import Vector

# dimensions of canvas
canvas_width = 1920
canvas_height = 1080

floor = Floor((0, canvas_height-90), (canvas_width-1, canvas_height-90), 90, "Grey")

# creating character
player = Player(floor, img_url="images/player.png", img_dest_dim=(60,60), position=Vector(500, 200))

enemy = Enemy(floor, canvas_width, character,speed=2, img_url="images/npc.png", img_dest_dim=(60,60))

all_entities = [player, floor, enemy]

gravity = Gravity(all_entities)

# creation of canvas
frame = simplegui.create_frame("Stick man", canvas_width, canvas_height, 0)
frame.set_canvas_background("White")

def draw(canvas: simplegui.Canvas):
    gravity.gravity()
    for entity in all_entities:
        entity.draw(canvas)

    # draw grid
    for i in range(canvas_width):
        if i % 60 == 0: canvas.draw_line((i, 0), (i, canvas_height), 2, 'black')
    for i in range(canvas_height):
        if i % 60 == 0: canvas.draw_line((0, i), (canvas_width, i), 2, 'black')


# setting handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(player.key_down)
frame.set_keyup_handler(player.key_up)

#frame.set_mousedrag_handler(pistol.point_to_mouse)

# starting frame
frame.start()