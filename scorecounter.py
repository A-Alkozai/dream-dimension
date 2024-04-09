class ScoreCounter:
    def __init__(self):
        self.WIDTH = 400
        self.HEIGHT = 100
        self.score = 0
        self.level = 0
        self.max_level = 0

    # Handler to draw on canvas
    def draw(self, canvas):
        canvas.draw_text("|| Score: " + str(self.score) + " || Level: " + str(self.level) + " ||", (100, 30), 30, 'White')

    # Handler to increase score
    def add_score(self, amount):
        self.score += amount

    # Handler to increase score when reaching new level
    def update_level(self, amount):
        self.level = amount
        if self.level > self.max_level:
            self.max_level = self.level
            self.score += 1
