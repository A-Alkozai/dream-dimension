# Globals live in this class
from player import Player
from vector import Vector

from enemy import Enemy
from map import MapManager
from interaction import Interaction
from healthbar import HealthBar
from entity import Entity

from scorecounter import ScoreCounter
from mana import ManaBar

from welcome_screen import WelcomeScreen

class GameState:
    def __init__(self, frame, width, height) -> None:
        self.CANVAS_WIDTH = width
        self.CANVAS_HEIGHT = height

        self.frame = frame

        self.all_entities = []
        self.player = None
        self.player_health = 3

        self.healthbar = HealthBar()
        self.scorecounter = ScoreCounter()
        self.mana_bar = ManaBar(self)

        self.interaction_manager = Interaction()

        self.player = Player('player',position=(0,0), game_manager=self, health=self.player_health)
        self.add_entity(self.player)

        # input handling for player
        self.frame.set_keydown_handler(self.player.key_down)
        self.frame.set_keyup_handler(self.player.key_up)
        
        self.map = MapManager(self)
        self.background = Background(self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        self.is_game_started = False
        # self.map.load()

        self.welcome_screen = WelcomeScreen(self)
        self.frame.set_mouseclick_handler(self.welcome_screen.mouse_click)
    
    def add_entity(self, entity):
        self.all_entities.append(entity)

    def remove_entity(self, entity):
        try: self.all_entities.remove(entity)
        except: pass

    def clear_screen(self):
        self.all_entities = []

    def load_map(self): self.map.load()

    def draw(self, canvas):
        self.background.draw(canvas)
        self.welcome_screen.draw(canvas)

        if not self.is_game_started: return
        self.healthbar.draw(canvas, self.player.health)
        self.scorecounter.draw(canvas)
        self.mana_bar.draw(canvas)

        for entity in self.all_entities:
            entity.update()
            entity.draw(canvas)

        if len(self.all_entities) > 0: self.interaction_manager.calculate_all_collisions(self.all_entities)

class Background(Entity):
    def __init__(self, canvas_width, canvas_height):
        super().__init__(position = Vector(canvas_width / 2, canvas_height / 2),
                         img_url="images/background.png",
                         img_dest_dim=(canvas_width, canvas_height))