import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


# Class to represent a health bar
class HealthBar:
    def __init__(self):
        self.heart_img = simplegui._load_local_image('images/heart.png')

    def draw(self, canvas, health):
        heart_img_dim = 50
        for i in range(health):
            position = ((heart_img_dim / 2) + (heart_img_dim * i) + 110, heart_img_dim / 2 + 35)
            canvas.draw_image(self.heart_img, (180, 180), (360, 360), position, (60, 60))
