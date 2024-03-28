import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class ScoreCounter:
    def __init__(self):
        self.WIDTH = 400
        self.HEIGHT = 100
        self.score = 0

    # Handler to draw on canvas
    def draw(self, canvas):
        canvas.draw_text("Score: " + str(self.score), (10, 40), 40, 'Black')

    # Handler to increase score
    def add_score(self, amount):
        self.score += amount
