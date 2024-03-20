import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from welcome_screen import WelcomeScreen
from vector import Vector
from player import Player
from enemy import Enemy
from map import Map


# dimensions of canvas
canvas_width = 1920
canvas_height = 1080


# Other game entities (player, enemy, etc.)
player = Player(walk=8, jump=2, attack=4, dmg=2, img_url="images/player.png", img_dest_dim=(60, 60), position=Vector(500, 200), row=12, column=8)

# Create a WelcomeScreen instance with canvas dimensions
welcome_screen = WelcomeScreen(canvas_width, canvas_height, player)

enemy1 = Enemy(range = False, canvas_width=canvas_width, player=player, walk=3, jump=2, attack=3,dmg=2, speed=0.8, img_url="images/orc_spearman.png", img_dest_dim=(60, 60), row=7, column=4)
enemy2 = Enemy(range = True, canvas_width=canvas_width, player=player, walk=3, jump=2, attack=3,dmg=2, speed=0.8, img_url="images/orc_crossbow.png", img_dest_dim=(60, 60), row=7, column=8)
enemy3 = Enemy(range = True,canvas_width=canvas_width, player=player, walk=3, jump=2, attack=3,dmg=2, speed=0.8, img_url="images/orc_hunter_mask_spritesheet.png", img_dest_dim=(60, 60), row=7, column=8)
map = Map(welcome_screen=welcome_screen)
all_entities = [player, enemy1, enemy2, enemy3, map]

# Create a frame
frame = simplegui.create_frame("Game", canvas_width, canvas_height)
frame.set_canvas_background("White")

# Keyboard event handlers
def key_down(key):
    player.key_down(key)

def key_up(key):
    player.key_up(key)

# Set keyboard handlers
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)



game_started  = False

# Draw handler for the frame
def draw(canvas):
    global game_started
    welcome_screen.draw(canvas)
    # Draw other entities if welcome screen is not showing
    if game_started:
        for entity in all_entities:
            entity.draw(canvas)
        for i in range(canvas_width):
            if i % 60 == 0:
                canvas.draw_line((i, 0), (i, canvas_height), 2, 'black')
        for i in range(canvas_height):
            if i % 60 == 0:
                canvas.draw_line((0, i), (canvas_width, i), 2, 'black')


# Mouse click handler for the frame
def mouse_click(pos):
    global game_started
    if welcome_screen.show_welcome_screen:
        if welcome_screen.play_button.contains_point(pos):
            welcome_screen.start_game()
            game_started = True
        elif welcome_screen.highscores_button.contains_point(pos):
            welcome_screen.show_highscores()
    elif welcome_screen.highscore_screen.show_highscores:  # Check if highscores screen is showing
        if welcome_screen.highscore_screen.back_button.contains_point(pos):
            welcome_screen.highscore_screen.go_back()


# Draw the frame
frame.set_draw_handler(draw)

# Set mouse click handler
frame.set_mouseclick_handler(mouse_click)


# Start the frame
frame.start()

