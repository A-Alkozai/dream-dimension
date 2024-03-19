import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class WelcomeScreen:
    def __init__(self, canvas_width, canvas_height):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.show_welcome_screen = True
        self.click_to_start = True

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

            # Draw click to start text
            if self.click_to_start:
                click_to_start_text = "Click to Start"
                canvas.draw_text(click_to_start_text, [(self.canvas_width - len(click_to_start_text) * 9) / 2, 220 + len(description_sentences) * 30], 24, welcome_color, "sans-serif")

    def start_game(self):
        self.show_welcome_screen = False

    def reset_game(self):
        self.show_welcome_screen = True
        # Reset lives and score here









