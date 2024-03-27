import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import object
from interaction import Interaction
interaction = Interaction()
current_map = 1
prev_map = 0


# Draw handler for the frame
def draw(canvas):
    if not game_started:
        object.welcome_screen.draw(canvas)
    # Draw other entities if welcome screen is not showing
    else:
        global prev_map
        if current_map != prev_map:
            object.map1.draw(canvas)
            object.set_entities(1)
            prev_map = current_map

        object.map1.draw(canvas)
        for entity in object.all_entities:
            if entity.SHOOTING:
                object.projectiles.append(entity.projectile)
                entity.SHOOTING = False
            if entity.DEAD:
                object.all_entities.remove(entity)
            entity.update()
            interaction.position_update(entity)
            entity.draw(canvas)

        for projectile in object.projectiles:
            if projectile.DEAD:
                object.projectiles.remove(projectile)
            projectile.update()
            interaction.position_update(projectile)
            projectile.draw(canvas)

        for i in range(object.canvas_width):
            if i % 60 == 0:
                canvas.draw_line((i, 0), (i, object.canvas_height), 2, 'black')
        for i in range(object.canvas_height):
            if i % 60 == 0:
                canvas.draw_line((0, i), (object.canvas_width, i), 2, 'black')


# Mouse click handler for the frame
def mouse_click(pos):
    global game_started
    if object.welcome_screen.show_welcome_screen:
        if object.welcome_screen.play_button.contains_point(pos):
            object.welcome_screen.start_game()
            game_started = True
        elif object.welcome_screen.highscores_button.contains_point(pos):
            object.welcome_screen.show_highscores()
    elif object.welcome_screen.highscore_screen.show_highscores:  # Check if highscores screen is showing
        if object.welcome_screen.highscore_screen.back_button.contains_point(pos):
            object.welcome_screen.highscore_screen.go_back()


# Create a frame
frame = simplegui.create_frame("Game", object.canvas_width, object.canvas_height, 0)
frame.set_canvas_background("White")

# Set keyboard handlers
frame.set_keydown_handler(object.player.key_down)
frame.set_keyup_handler(object.player.key_up)
game_started = False

# Set mouse click handler
frame.set_mouseclick_handler(mouse_click)

# Draw the frame
frame.set_draw_handler(draw)

# Start the frame
frame.start()
