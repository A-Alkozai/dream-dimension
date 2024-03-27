import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
# import object
from interaction import Interaction
from GameState import GameState
from map import MapManager

gameManager = GameState()


interaction = Interaction()
current_map = 1
prev_map = 0

def draw(canvas):
    # object.map1.draw(canvas)
    gameManager.draw(canvas)

    for i in range(gameManager.CANVAS_WIDTH):
        if i % 60 == 0:
            canvas.draw_line((i, 0), (i, gameManager.CANVAS_HEIGHT), 2, 'black')
    for i in range(gameManager.CANVAS_HEIGHT):
        if i % 60 == 0:
            canvas.draw_line((0, i), (gameManager.CANVAS_WIDTH, i), 2, 'black')




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


# Create a frame
frame = simplegui.create_frame("Game", gameManager.CANVAS_WIDTH, gameManager.CANVAS_HEIGHT, 0)
frame.set_canvas_background("White")

# Set keyboard handlers
frame.set_keydown_handler(gameManager.player.key_down)
frame.set_keyup_handler(gameManager.player.key_up)
game_started = False

# Set mouse click handler
# frame.set_mouseclick_handler(mouse_click)

# Draw the frame
frame.set_draw_handler(draw)

# Start the frame
frame.start()
