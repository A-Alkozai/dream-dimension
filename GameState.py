# Globals live in this class
from entity import Entity
from player import Player
from interaction import Interaction

from map import MapManager
from vector import Vector

from scorecounter import ScoreCounter
from healthbar import HealthBar
from mana_bar import ManaBar
from slot import Slot

from welcome_screen import WelcomeScreen


class GameState:
    def __init__(self, frame, width, height) -> None:
        self.CANVAS_WIDTH = width
        self.CANVAS_HEIGHT = height

        self.frame = frame

        self.all_entities = []
        self.all_texts = []
        self.player = None
        self.player_health = 3

        self.score_counter = ScoreCounter()
        self.health_bar = HealthBar()
        self.mana_bar = ManaBar(self)
        self.slot = Slot(self)

        self.interaction_manager = Interaction()

        # Create and add to list
        self.player = Player(kind='player', position=Vector(0, 0), game_manager=self, lives=self.player_health,
                             img_url='images/sprites/player/player.png', row=13, column=8, img_dest_dim=(60, 60))
        self.add_entity(self.player)

        # Input handling for player
        self.frame.set_keydown_handler(self.player.key_down)
        self.frame.set_keyup_handler(self.player.key_up)

        # Create map and background
        self.map = MapManager(self)
        self.background = Background(self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        self.is_game_started = False
        self.is_story_finished = False

        # Create welcome screen
        self.welcome_screen = WelcomeScreen(self, self.interaction_manager)
        self.frame.set_mouseclick_handler(self.welcome_screen.mouse_click)

    def add_text(self, text):
        self.all_texts.append(text)

    def add_entity(self, entity):
        self.all_entities.append(entity)

    def remove_entity(self, entity):
        try:
            self.all_entities.remove(entity)
        except:
            pass

    # Removes all entities being drawn
    def clear_screen(self):
        self.all_entities = []

    # The draw handler
    def draw(self, canvas):
        # Determine background based on room level
        if self.map.current_room_index == 0:
            self.background.change_image('images/jungle/ForestBG2_lite.png')
        elif self.map.current_room_index == 4:
            self.background.change_image('images/jungle/ForestBG7_lite.png')
        elif self.map.current_room_index == 5:
            self.background.change_image('images/dungeon/CaveBG1_lite.png')

        # Draw background and welcome screen
        self.background.draw(canvas)
        self.welcome_screen.draw(canvas)

        # Continues drawing only if game has started
        if not self.is_game_started:
            return

        # Update then draw entities
        for entity in self.all_entities:
            entity.update()
            entity.draw(canvas)

        # Calculate all collisions for all entities
        if len(self.all_entities) > 0:
            self.interaction_manager.calculate_all_collisions(self.all_entities)

        # Widgets being drawn
        self.health_bar.draw(canvas, self.player.lives)
        self.score_counter.draw(canvas)
        self.mana_bar.draw(canvas)
        self.slot.update()
        self.slot.draw(canvas)

        # Text being drawn
        for text in self.all_texts:
            text.draw(canvas)
            self.all_texts.remove(text)


# Initialises Background
class Background(Entity):
    def __init__(self, canvas_width, canvas_height):
        super().__init__(position=Vector(canvas_width / 2, canvas_height / 2),
                         img_url="images/jungle/ForestBG2_lite.png", img_dest_dim=(canvas_width, canvas_height))
