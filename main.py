import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from welcome_screen import WelcomeScreen
from vector import Vector
from player import Player
from enemy import Enemy
from map import Map

# dimensions of canvas
canvas_width = 1920
canvas_height = 1080

# Create a frame
frame = simplegui.create_frame("Game", canvas_width, canvas_height)

# Create a WelcomeScreen instance with canvas dimensions
welcome_screen = WelcomeScreen(canvas_width, canvas_height)

welcome_background_colour = "black"
game_background_colour = "white"

# Keyboard event handlers
def key_down(key):
    player.key_down(key)

def key_up(key):
    player.key_up(key)

# Set keyboard handlers
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)

# Draw handler for the frame
def draw(canvas):
    # Draw welcome screen
    welcome_screen.draw(canvas)
    # Draw other entities if welcome screen is not showing
    if not welcome_screen.show_welcome_screen:
        for entity in all_entities:
            entity.draw(canvas)

# Mouse click handler for the frame
def mouse_click(pos):
    # If welcome screen is showing and clicked, start the game
    if welcome_screen.show_welcome_screen:
        welcome_screen.start_game()

# Set mouse click handler
frame.set_mouseclick_handler(mouse_click)

# Other game entities (player, enemy, etc.)
player = Player(welcome_screen=welcome_screen, walk=8, jump=2, attack=4, dmg=2, img_url="images/player.png", img_dest_dim=(60, 60), position=Vector(500, 200), row=12, column=8)

enemy = Enemy(canvas_width=canvas_width, welcome_screen=welcome_screen, player=player, walk=3, jump=2, attack=3,dmg=2, speed=0.8, img_url="images/orc_spearman.png", img_dest_dim=(60, 60), row=7, column=4)

map = Map(welcome_screen=welcome_screen)

all_entities = [player, enemy, map]

# Draw the frame
frame.set_draw_handler(draw)

# Start the frame
frame.start()

