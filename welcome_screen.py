import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from highscore_screen import HighscoreScreen


class Button:
    def __init__(self, label, pos, width, height, action):
        self.label = label
        self.pos = pos
        self.width = width
        self.height = height
        self.action = action
        
    def draw(self, canvas):
        label_width = len(self.label) * 12
        label_height = 24
        canvas.draw_text(self.label, (self.pos[0] - label_width / 2, self.pos[1] + label_height / 4), 24, "White")
        canvas.draw_polygon([(self.pos[0] - self.width / 2, self.pos[1] - self.height / 2),
                             (self.pos[0] + self.width / 2, self.pos[1] - self.height / 2),
                             (self.pos[0] + self.width / 2, self.pos[1] + self.height / 2),
                             (self.pos[0] - self.width / 2, self.pos[1] + self.height / 2)], 1, "White")

    def contains_point(self, pos):
        x_in_range = pos[0] >= self.pos[0] - self.width / 2 and pos[0] <= self.pos[0] + self.width / 2
        y_in_range = pos[1] >= self.pos[1] - self.height / 2 and pos[1] <= self.pos[1] + self.height / 2
        return x_in_range and y_in_range


class WelcomeScreen:
    def __init__(self, canvas_width, canvas_height, player):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.show_welcome_screen = True
        self.player = player
        self.highscores_shown = False
        self.highscore_screen = HighscoreScreen(canvas_width, canvas_height, [], self)  # Initialize HighscoreScreen
        
        # Define button dimensions and positions
        button_width = 200
        button_height = 50
        button_margin = 20
        button_x = canvas_width / 2
        play_button_y = canvas_height * 3 / 4 - button_height - button_margin
        highscores_button_y = canvas_height * 3 / 4 + button_margin

        self.play_button = Button("Play/Start", (button_x, play_button_y), button_width, button_height, self.start_game)
        self.highscores_button = Button("Highscores", (button_x, highscores_button_y), button_width, button_height, self.show_highscores)

    def draw(self, canvas):
        if self.show_welcome_screen:
            # Draw background gradient
            gradient_color_top = "LightSkyBlue"
            gradient_color_bottom = "SkyBlue"
            canvas.draw_polygon([(0, 0), (self.canvas_width, 0), (self.canvas_width, self.canvas_height), (0, self.canvas_height)], 1, gradient_color_top, gradient_color_bottom)

            # Draw border
            border_color = "DarkBlue"
            border_width = 2
            canvas.draw_polygon([(border_width, border_width), (self.canvas_width - border_width, border_width),
                                 (self.canvas_width - border_width, self.canvas_height - border_width),
                                 (border_width, self.canvas_height - border_width)], border_width, border_color)

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
            self.play_button.draw(canvas)
            self.highscores_button.draw(canvas)

        elif self.highscores_shown:
            self.highscore_screen.draw(canvas)  # Draw HighscoreScreen if highscores are shown

    def start_game(self):
        self.show_welcome_screen = False

    def show_highscores(self):
        self.show_welcome_screen = False
        self.highscores_shown = True
        self.highscore_screen.show_highscores([("Player", self.player.points)])  # Pass player's name and points

    def hide_highscores(self):
        self.highscores_shown = False

    def reset_game(self):
        self.show_welcome_screen = True
        # Reset lives and score here
