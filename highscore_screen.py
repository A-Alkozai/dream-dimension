from entity import Entity
from vector import Vector


class Background(Entity):
    def __init__(self, canvas_width, canvas_height, img_url):
        super().__init__(position=Vector(canvas_width/2, canvas_height/2), img_url=img_url, img_dest_dim=(canvas_width, canvas_height))


class HighscoreScreen:
    def __init__(self, welcome_screen):
        self.canvas_width = welcome_screen.canvas_width
        self.canvas_height = welcome_screen.canvas_height
        self.welcome_screen = welcome_screen
        self.show_highscores_screen = False

        # Score tracking
        self.scores = []
        self.highscore = 0

        # Creating background and back_button
        self.background_entity = Background(self.canvas_width, self.canvas_height, "images/main_menu_bg.jpg")
        self.back_button = Entity(kind='button', position=Vector(200, 1000), img_url="images/buttons/back.png", img_dest_dim=(286*1.3, 140*1.3))

    def draw(self, canvas):
        if self.show_highscores_screen:
            # Draw background
            self.background_entity.draw(canvas)

            # Draw title
            title = Entity(kind='text', position=Vector(self.canvas_width / 2, 170), img_url="images/texts/score_tracker.png", img_dest_dim=(467*1.6, 136*1.6))
            title.draw(canvas)

            # Draw highscore title
            highscore = Entity(kind='text', position=Vector(420, 270), img_url="images/texts/highscore.png", img_dest_dim=(467*0.8, 136*0.8))
            highscore.draw(canvas)

            # Draw the highest score
            if not self.scores:
                self.highscore = 0
            else:
                self.highscore = max(self.scores)
            highscore_text = str(self.highscore)
            highscore_font = 60
            highscore_position = (highscore.position.x + 180, 290)
            canvas.draw_text(highscore_text, highscore_position, highscore_font, "White")

            # Draw all scores
            attempt = 1
            score_font = 25
            score_position = [highscore.position.x, 370]
            for score in self.scores:
                score_text = f"Attempt {attempt}:  {score}"
                canvas.draw_text(score_text, score_position, score_font, "White")
                score_position[1] += 60
                attempt += 1
                if score_position[1] >= 370+(60*10):
                    score_position = [score_position[0] + 250, 370]

            # Draw back button
            self.back_button.draw(canvas)

    def show_highscore(self):
        self.show_highscores_screen = True

    def go_back(self):
        self.show_highscores_screen = False
        self.welcome_screen.show_welcome_screen = True
