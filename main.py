import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
# import object
from interaction import Interaction
from GameState import GameState
from map import MapManager




interaction = Interaction()
current_map = 1
prev_map = 0

def draw(canvas):
    # object.map1.draw(canvas)
    game_manager.draw(canvas)

    # for i in range(game_manager.CANVAS_WIDTH):
    #     if i % 60 == 0:
    #         canvas.draw_line((i, 0), (i, game_manager.CANVAS_HEIGHT), 2, 'black')
    # for i in range(game_manager.CANVAS_HEIGHT):
    #     if i % 60 == 0:
    #         canvas.draw_line((0, i), (game_manager.CANVAS_WIDTH, i), 2, 'black')




# # Mouse click handler for the frame
# def mouse_click(pos):
#     global game_started
#     if object.welcome_screen.show_welcome_screen:
#         if object.welcome_screen.play_button.contains_point(pos):
#             object.welcome_screen.start_game()
#             game_started = True
#         elif object.welcome_screen.highscores_button.contains_point(pos):
#             object.welcome_screen.show_highscores()
#     elif object.welcome_screen.highscore_screen.show_highscores:  # Check if highscores screen is showing
#         if object.welcome_screen.highscore_screen.back_button.contains_point(pos):
#             object.welcome_screen.highscore_screen.go_back()

CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080

# Create a frame
frame = simplegui.create_frame("Game", CANVAS_WIDTH, CANVAS_HEIGHT, 0)
frame.set_canvas_background("White")

game_manager = GameState(frame, CANVAS_WIDTH, CANVAS_HEIGHT)

# Set keyboard handlers
game_started = False

# Set mouse click handler
# frame.set_mouseclick_handler(mouse_click)

# Draw the frame
frame.set_draw_handler(draw)

# Start the frame
frame.start()
