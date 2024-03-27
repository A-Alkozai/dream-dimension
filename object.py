from welcome_screen import WelcomeScreen
from vector import Vector
from player import Player
from enemy import Enemy
from map import Map

# dimensions of canvas
canvas_width = 1920
canvas_height = 1080


# Create player
player = Player(walk_frames=8, jump_frames=2, attack_frames=4, dmg_frames=2, img_url="images/player.png",
                img_dest_dim=(60, 60), position=Vector(500, 200), row=13, column=8)

# Create enemies
enemy1 = Enemy(is_ranged=False, player=player, walk_frames=3, jump_frames=2, attack_frames=3,
               dmg_frames=2, speed=0.6, img_url="images/orc_warrior.png", img_dest_dim=(50, 60),
               position=Vector(100, 100), row=7, column=4)
enemy2 = Enemy(is_ranged=True, player=player, walk_frames=3, jump_frames=2, attack_frames=4,
               dmg_frames=2, speed=0.4, img_url="images/orc_hunter.png", img_dest_dim=(50, 60),
               position=Vector(900, 100), row=7, column=8)
enemy3 = Enemy(is_ranged=True, player=player, walk_frames=3, jump_frames=2, attack_frames=4,
               dmg_frames=2, speed=0.4, img_url="images/orc_shaman.png", img_dest_dim=(50, 60),
               position=Vector(1000, 100), row=7, column=8)

# Create a WelcomeScreen instance with canvas dimensions
welcome_screen = WelcomeScreen(canvas_width, canvas_height, player)
map1 = Map(welcome_screen=welcome_screen)
map2 = None

# Map 1 entities
map1_enemies = [enemy1, enemy2, enemy3]
map1_entities = [enemy1, enemy2, enemy3, player]

# Entities that get draw
projectiles = []
blocks = list(map1.tiles)
players = [player]
enemies = [x for x in map1_enemies]
all_entities = [x for x in enemies]
all_entities.append(player)


def set_entities(map_number):
    global projectiles, enemies, blocks, all_entities
    if map_number == 1:
        projectiles = []
        blocks = list(map1.tiles)
        enemies = [x for x in map1_enemies]
        all_entities = [x for x in enemies]
        all_entities.append(player)
