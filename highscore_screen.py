import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

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


class HighscoreScreen:
    def __init__(self, canvas_width, canvas_height, highscores, welcome_screen):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.show_highscores_screen = False
        self.highscores = highscores
        self.welcome_screen = welcome_screen
        
        # Define button dimensions and positions
        button_width = 200
        button_height = 50
        button_margin = 20
        button_x = canvas_width / 2
        back_button_y = canvas_height * 3 / 4 + button_margin

        self.back_button = Button("Back", (button_x, back_button_y), button_width, button_height, self.go_back)

    def draw(self, canvas):
        if self.show_highscores_screen:
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

            # Draw highscores text
            title_font_size = 36
            highscores_font_size = 24
            title = "Highscores"
            highscores_y = self.canvas_height / 4
            title_position = ((self.canvas_width - len(title) * title_font_size) / 2, highscores_y)
            canvas.draw_text(title, title_position, title_font_size, "Black")
            
            # Draw highscores
            highscores_start_y = highscores_y + title_font_size + 20
            for i, (player, score) in enumerate(self.highscores, start=1):
                highscores_text = f"{i}. {player} - {score}"  # Corrected line
                highscores_position = ((self.canvas_width - len(highscores_text) * highscores_font_size) / 2, highscores_start_y + i * 40)  # Corrected line
                canvas.draw_text(highscores_text, highscores_position, highscores_font_size, "Black")
                
            # Draw back button
            self.back_button.draw(canvas)

    def show_highscores(self, highscores):
        self.highscores = highscores
        self.show_highscores_screen = True

    def go_back(self):
        self.show_highscores_screen = False
        self.welcome_screen.show_welcome_screen = True

