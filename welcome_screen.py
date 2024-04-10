from story_screen import StoryScreen
from highscore_screen import HighscoreScreen
from control_screen import ControlScreen
from credit_screen import CreditScreen
from entity import Entity
from vector import Vector


class Background(Entity):
    def __init__(self, canvas_width, canvas_height):
        super().__init__(position=Vector(canvas_width/2, canvas_height/2),
                         img_url="images/main_menu_bg.jpg",
                         img_dest_dim=(canvas_width, canvas_height))


class WelcomeScreen:
    def __init__(self, game_manager, interaction):
        self.game_manager = game_manager
        self.interaction = interaction

        self.canvas_width = game_manager.CANVAS_WIDTH
        self.canvas_height = game_manager.CANVAS_HEIGHT

        # Initialise content displayed
        self.show_welcome_screen = True
        self.story_shown = False
        self.highscore_shown = False
        self.controls_shown = False
        self.credits_shown = False

        # Initialise the different displays
        self.story_screen = StoryScreen(self)
        self.highscore_screen = HighscoreScreen(self)
        self.control_screen = ControlScreen(self)
        self.credit_screen = CreditScreen(self)
        self.background_entity = Background(self.canvas_width, self.canvas_height)

        # Initialise the 4 buttons
        self.play_button = Entity(kind='button', position=Vector(self.canvas_width / 2, 315), img_url="images/buttons/start_game.png", img_dest_dim=(520, 92))

        self.highscore_button = Entity(kind='button', position=Vector(self.canvas_width / 2, 425), img_url="images/buttons/highscore.png", img_dest_dim=(371, 82))

        self.controls_button = Entity(kind='button', position=Vector(self.canvas_width / 2, 525), img_url="images/buttons/controls.png", img_dest_dim=(346, 81))

        self.credits_button = Entity(kind='button', position=Vector(self.canvas_width / 2, 625), img_url="images/buttons/credits.png", img_dest_dim=(296, 82))

    def draw(self, canvas):
        if self.show_welcome_screen:
            self.background_entity.draw(canvas)

            # Draw buttons
            self.play_button.draw(canvas)
            self.highscore_button.draw(canvas)
            self.controls_button.draw(canvas)
            self.credits_button.draw(canvas)

        # Draws the other screens if toggled on
        elif self.story_shown:
            self.story_screen.draw(canvas)

        elif self.highscore_shown:
            self.highscore_screen.draw(canvas)

        elif self.controls_shown:
            self.control_screen.draw(canvas)

        elif self.credits_shown:
            self.credit_screen.draw(canvas)
    
    def mouse_click(self, pos):
        mouse_entity = Entity(position=Vector(pos[0], pos[1]))
        if self.show_welcome_screen:
            # Check if play_button clicked
            if self.interaction.is_overlapping(mouse_entity, self.play_button):
                self.show_story()

            # Check if highscore_button clicked
            elif self.interaction.is_overlapping(mouse_entity, self.highscore_button):
                self.show_highscores()

            # Check if controls_button clicked
            elif self.interaction.is_overlapping(mouse_entity, self.controls_button):
                self.show_controls()

            # Check if credits_button clicked
            elif self.interaction.is_overlapping(mouse_entity, self.credits_button):
                self.show_credits()

        # If story screen is showing
        elif self.story_shown:
            if self.story_screen.screen1:
                if self.interaction.is_overlapping(mouse_entity, self.story_screen.choice1):
                    self.story_screen.screen1 = False
                    self.story_screen.screen2 = True
            elif self.story_screen.screen2:
                if self.interaction.is_overlapping(mouse_entity, self.story_screen.choice2):
                    self.story_screen.screen2 = False
                    self.story_screen.screen3 = True
            elif self.story_screen.screen3:
                if self.interaction.is_overlapping(mouse_entity, self.story_screen.choice3):
                    self.story_screen.hide_story()
                    self.start_game()
                    self.game_manager.score_counter.score = 0

        # If highscore screen is showing
        elif self.highscore_shown:
            if self.interaction.is_overlapping(mouse_entity, self.highscore_screen.back_button):
                self.highscore_screen.go_back()

        # If controls screen is showing
        elif self.controls_shown: 
            if self.interaction.is_overlapping(mouse_entity, self.control_screen.back_button):
                self.control_screen.go_back()

        # If credits screen is showing
        elif self.credits_shown:
            if self.interaction.is_overlapping(mouse_entity, self.credit_screen.back_button):
                self.control_screen.go_back()

    def start_game(self):
        self.show_welcome_screen = False
        self.game_manager.is_game_started = True
        self.game_manager.map.current_room_index = -1
        self.game_manager.map.change_room(1)
        self.game_manager.player.lives = 3
        self.game_manager.player.mana = self.game_manager.player.mana_max

    def show_story(self):
        self.show_welcome_screen = False
        self.hide_highscores()
        self.hide_controls()
        self.hide_credits()
        self.story_shown = True
        self.story_screen.show_story()

    def hide_story(self):
        self.story_shown = False

    def show_highscores(self):
        self.show_welcome_screen = False
        self.hide_story()
        self.hide_controls()
        self.hide_credits()
        self.highscore_shown = True
        self.highscore_screen.show_highscore()
        # self.highscore_screen.show_highscores([("Player", self.game_manager.score_counter.score)])  # Pass player's name and points

    def hide_highscores(self):
        self.highscore_shown = False

    def show_controls(self):
        self.show_welcome_screen = False
        self.hide_story()
        self.hide_highscores()
        self.hide_credits()
        self.controls_shown = True
        self.control_screen.show_controls()

    def hide_controls(self):
        self.controls_shown = False

    def show_credits(self):
        self.show_welcome_screen = False
        self.hide_story()
        self.hide_highscores()
        self.hide_controls()
        self.credits_shown = True
        self.credit_screen.show_credits()
    
    def hide_credits(self):
        self.credits_shown = False

    def reset_game(self):
        self.show_welcome_screen = True
