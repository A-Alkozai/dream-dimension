from highscore_screen import HighscoreScreen
from control_screen import ControlScreen
from credit_screen import CreditScreen
from entity import Entity
from vector import Vector


class Background(Entity):
    def __init__(self, canvas_width, canvas_height, img_url):
        super().__init__(position = Vector(canvas_width / 2, canvas_height / 2),
                         img_url="images/background.png",
                         img_dest_dim=(canvas_width, canvas_height))


class PlayButton(Entity):
    def __init__(self, canvas_width, canvas_height, img_url):
        super().__init__(position = Vector(canvas_width / 2, canvas_height *3 / 4 -50), img_url= "images/play_button.png")


class HighscoresButton(Entity):
    def __init__(self, canvas_width, canvas_height, img_url):
        super().__init__(position=Vector(canvas_width / 2, canvas_height * 3 / 4 + 150), img_url="images/highscores_button.png")


class ControlsButton(Entity):
    def __init__(self, canvas_width, canvas_height, img_url):
        super().__init__(position=Vector(canvas_width / 2, canvas_height * 3 / 4 + 100), img_url="images/controls_button.png")


class CreditsButton(Entity):
    def __init__(self, canvas_width, canvas_height, img_url):
        super().__init__(position=Vector(canvas_width - 100, canvas_height - 50), img_url="images/credits_button.png")


class WelcomeScreen:
    def __init__(self, game_manager):
        self.game_manager = game_manager

        self.canvas_width = game_manager.CANVAS_WIDTH
        self.canvas_height = game_manager.CANVAS_HEIGHT
        self.show_welcome_screen = True

        self.highscores_shown = False
        self.highscore_screen = HighscoreScreen(self.canvas_width, self.canvas_height, self)  
        
        self.controls_shown = False
        self.control_screen = ControlScreen(self.canvas_width, self.canvas_height, self)

        self.credits_shown = False
        self.credit_screen = CreditScreen(self.canvas_width, self.canvas_height, self)
        
        self.background_entity = Background(self.canvas_width, self.canvas_height, "images/background.png")

        #button_spacing = 50
        left_button_x = self.canvas_width / 4
        right_button_x = self.canvas_width * 3 / 4
        
        self.play_button_entity = PlayButton(self.canvas_width, self.canvas_height, "images/play_button.png")
        self.play_button_entity.position = Vector(left_button_x, 700)

        self.highscores_button_entity = HighscoresButton(self.canvas_width, self.canvas_height, "images/highscores_button.png")
        self.highscores_button_entity.position = Vector(right_button_x, 700)

        self.controls_button_entity = ControlsButton(self.canvas_width, self.canvas_height, "images/controls_button.png")
        self.controls_button_entity.position = Vector(self.canvas_width / 2, self.canvas_height * 3 / 4 + 150)

        self.credits_button_entity = CreditsButton(self.canvas_width, self.canvas_height, "images/credits_button.png")
        self.credits_button_entity.position = Vector(self.canvas_width -100, self.canvas_height -50)
    
    def draw(self, canvas):
        if self.show_welcome_screen:
        
            self.background_entity.draw(canvas)

            # Draw welcome text
            welcome_text = "Welcome to the Game!"
            welcome_color = "White"
            canvas.draw_text(welcome_text, [(self.canvas_width - len(welcome_text) * 12) / 2, 150], 36, welcome_color, "sans-serif")

            # Draw description text
            description_text = ("You are in Royal Holloway, and you have a Project due in tomorrow. "
                                "You want to complete that project that day, so you walk into the library. "
                                "You see free muffins, and you take one. You make your way to silent study. "
                                "You take a bite....And now you suddenly get teleported to a different dimension. "
                                "GOAL: To escape the dimension error and go back to reality to complete your Project")

            description_sentences = description_text.split(". ")  # Split into separate sentences

            # Draw each sentence underneath each other with more spacing
            for i, sentence in enumerate(description_sentences):
                canvas.draw_text(sentence, [(self.canvas_width - len(sentence) * 6) / 2, 220 + i * 30], 18, welcome_color, "sans-serif")

            # Draw buttons
            self.play_button_entity.draw(canvas)
            self.highscores_button_entity.draw(canvas)
            self.controls_button_entity.draw(canvas)
            self.credits_button_entity.draw(canvas)

        elif self.highscores_shown:
            self.highscore_screen.draw(canvas)  # Draw HighscoreScreen if highscores are shown

        elif self.controls_shown:
            self.control_screen.draw(canvas) #Draw ControlScreen if control screen button clicked

        elif self.credits_shown:
            self.credit_screen.draw(canvas)
    
    def mouse_click(self, pos):
        if self.show_welcome_screen:

            play_button_distance = ((pos[0] - self.play_button_entity.position.x) ** 2 + 
                                    (pos[1] - self.play_button_entity.position.y) ** 2) ** 0.5
            
            highscores_button_distance = ((pos[0] - self.highscores_button_entity.position.x) ** 2 +
                                        (pos[1] - self.highscores_button_entity.position.y) ** 2) ** 0.5
            
            controls_button_distance = ((pos[0] - self.controls_button_entity.position.x) ** 2 +
                                    (pos[1] - self.controls_button_entity.position.y) ** 2) ** 0.5
            
            credits_button_distance = ((pos[0] - self.credits_button_entity.position.x) ** 2 +
                                    (pos[1] - self.credits_button_entity.position.y) ** 2) ** 0.5
            

            if play_button_distance < self.play_button_entity.img_dest_dim[0] / 2:
                self.start_game()
                self.game_manager.score_counter.score = 0
                game_started = True

            elif highscores_button_distance < self.highscores_button_entity.img_dest_dim[0] / 2:
                self.show_highscores()

            elif controls_button_distance < self.controls_button_entity.img_dest_dim[0] / 2:
                self.show_controls()

            elif credits_button_distance < self.credits_button_entity.img_dest_dim[0] / 2:
                self.show_credits()
            
        elif self.highscores_shown:  # Check if highscores screen is showing
            if self.highscore_screen.back_button.contains_point(pos):
                self.highscore_screen.go_back()

        elif self.controls_shown: 
            if self.control_screen.back_button.contains_point(pos):
                self.control_screen.go_back()
        
        elif self.credits_shown:
            if self.credit_screen.back_button.contains_point(pos):
                self.control_screen.go_back()


    def start_game(self):
        self.show_welcome_screen = False
        self.game_manager.is_game_started = True
        self.game_manager.map.current_room_index = -1
        self.game_manager.map.change_room(1)
        self.game_manager.player.lives = 3
        self.game_manager.player.mana = self.game_manager.player.mana_max

    def show_highscores(self):
        self.show_welcome_screen = False
        self.hide_controls()
        self.hide_credits()
        self.highscores_shown = True
        self.highscore_screen.show_highscores([("Player", self.game_manager.score_counter.score)])  # Pass player's name and points

    def hide_highscores(self):
        self.highscores_shown = False

    def show_controls(self):
        self.show_welcome_screen = False
        self.hide_highscores()
        self.hide_credits()
        self.controls_shown = True
        self.control_screen.show_controls()

    def hide_controls(self):
        self.controls_shown = False

    def show_credits(self):
        self.show_welcome_screen = False
        self.hide_highscores()
        self.hide_controls()
        self.credits_shown = True
        self.credit_screen.show_credits()
    
    def hide_credits(self):
        self.credits_shown = False

    def reset_game(self):
        self.show_welcome_screen = True
        # Reset lives and score here
