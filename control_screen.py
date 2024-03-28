import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from entity import Entity
from vector import Vector

class Background(Entity):
    def __init__(self, canvas_width, canvas_height, img_url):
        super().__init__(position = Vector(canvas_width / 2, canvas_height / 2),
                         img_url="images/background.png",
                         img_dest_dim=(canvas_width, canvas_height))

class BackButton(Entity):
    def __init__(self, canvas_width, canvas_height, img_url, goback):
        super().__init__(position=Vector(canvas_width / 2, canvas_height * 3 / 4 + 50), img_url="images/back_button.png")
        self.goback = goback

    def contains_point(self, pos):
        x_in_range = pos[0] >= self.position.x - self.img_dest_dim[0] / 2 and pos[0] <= self.position.x + self.img_dest_dim[0] / 2
        y_in_range = pos[1] >= self.position.y - self.img_dest_dim[1] / 2 and pos[1] <= self.position.y + self.img_dest_dim[1] / 2
        return x_in_range and y_in_range
    
class ControlScreen:
    def __init__(self, canvas_width, canvas_height, welcome_screen):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.show_controls_screen = False
        self.welcome_screen = welcome_screen

        button_width = 400  # Adjust as needed
        button_height = 50  # Adjust as needed
        button_margin = 20  # Adjust as needed
        back_button_x = canvas_width - button_width / 2 - button_margin
        back_button_y = canvas_height - button_height / 2 - button_margin
        
        self.background_entity = Background(canvas_width, canvas_height, "images/background.png")
        self.back_button = BackButton(back_button_x, back_button_y, "images/back.png", self.go_back)

        self.controls_text = [
            "A/D: Move Left/Right",
            "W: Climb ladders",
            "Spacebar: Jump",
            "F: Punch",
            "Q: Shoot"
        ]

    def draw(self, canvas):
        if self.show_controls_screen:

            self.background_entity.draw(canvas)

            # Draw highscores text
            title_font_size = 48
            title = "Controls"
            controls_y = self.canvas_height / 4
            title_position = ((self.canvas_width - len(title) * title_font_size) / 2, controls_y)
            canvas.draw_text(title, title_position, title_font_size, "White")
            
            text_start_y = controls_y + title_font_size + 40  # Start below the title
            line_height = 30  # Adjust as needed
            for i, line in enumerate(self.controls_text):
                #text_width = len(line) * (line_height / 2)  # Manually calculate text width
                text_x = 750
                text_y = text_start_y + i * line_height
                canvas.draw_text(line, (text_x, text_y), line_height, "White")
                    
            # Draw back button
            self.back_button.draw(canvas)

    def show_controls(self):
        self.show_controls_screen = True

    def go_back(self):
        self.show_controls_screen = False
        self.welcome_screen.show_welcome_screen = True
        self.welcome_screen.credits_shown = False
