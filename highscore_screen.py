from entity import Entity
from vector import Vector


class Background(Entity):
    def __init__(self, canvas_width, canvas_height, img_url):
        super().__init__(position=Vector(canvas_width / 2, canvas_height / 2),
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
    

class HighscoreScreen:
    def __init__(self, canvas_width, canvas_height, welcome_screen):
        
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.show_highscores_screen = False
        self.scores = []
        self.highscore = 0
        self.welcome_screen = welcome_screen

        button_width = 400  # Adjust as needed
        button_height = 50  # Adjust as needed
        button_margin = 20  # Adjust as needed
        back_button_x = self.canvas_width - button_width / 2 - button_margin
        back_button_y = self.canvas_height - button_height / 2 - button_margin
        
        self.background_entity = Background(self.canvas_width, self.canvas_height, "images/background.png")
        self.back_button = BackButton(back_button_x, back_button_y, "images/back.png", self.go_back)

    def draw(self, canvas):
        if self.show_highscores_screen:

            # Draw background
            self.background_entity.draw(canvas)

            # Draw title
            title_font_size = 60
            title = "|| Score Tracker ||"
            title_position = ((self.canvas_width - len(title) * title_font_size) / 2, 180)
            canvas.draw_text(title, title_position, title_font_size, "White")

            # Draw the highest score
            if not self.scores:
                self.highscore = 0
            else:
                self.highscore = max(self.scores)
            highscore_text = f"<<< Highscore: {self.highscore} >>>"
            highscore_font = 40
            highscore_position = ((self.canvas_width - len(title) * title_font_size) / 2, 280)
            canvas.draw_text(highscore_text, highscore_position, highscore_font, "White")

            # Draw all scores
            attempt = 1
            score_font = 25
            score_position = [(self.canvas_width - len(title) * title_font_size) / 2, 340]
            for score in self.scores:
                score_text = f"Attempt {attempt}:  {score}"
                canvas.draw_text(score_text, score_position, score_font, "White")
                score_position[1] += 30
                attempt += 1
                if score_position[1] == 340+(30*15):
                    score_position = [score_position[0] + 250, 340]

            # Draw back button
            self.back_button.draw(canvas)

    def show_highscores(self, highscores):
        self.highscores = highscores
        self.show_highscores_screen = True

    def go_back(self):
        self.show_highscores_screen = False
        self.welcome_screen.show_welcome_screen = True