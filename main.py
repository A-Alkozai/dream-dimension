import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from interaction import Interaction
from GameState import GameState

interaction = Interaction()
current_map = 1
prev_map = 0


def draw(canvas):
    game_manager.draw(canvas)


CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080

# Create a frame
frame = simplegui.create_frame("Game", CANVAS_WIDTH, CANVAS_HEIGHT, 0)
frame.set_canvas_background("White")

game_manager = GameState(frame, CANVAS_WIDTH, CANVAS_HEIGHT)

# Set keyboard handlers
game_started = False

# Draw the frame
frame.set_draw_handler(draw)

# Start the frame
frame.start()

# Current problems:
# - Weird block collisions

