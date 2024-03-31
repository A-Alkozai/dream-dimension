import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


# Class to represent a health bar
class HealthBar():
    def __init__(self):
        # super().__init__('healthbar', **kwargs)

        self.heart_img = simplegui._load_local_image('images/heart.png')

    def draw(self, canvas, health):
        heart_img_dim = 60
        for i in range(health):
            position = ((heart_img_dim / 2) + (heart_img_dim * i), heart_img_dim / 2 + 35)
            canvas.draw_image(self.heart_img, (180,180), (360,360), position, (60,60))


# # Draw handler function for the frame
# def draw(canvas):
#     global health_bar, num_hearts

#     # Draw the health bar on the canvas
#     health_bar.draw(canvas)
#     # Draw the hearts
#     for i in range(num_hearts):
#         canvas.draw_image(heart_image, (heart_image.get_width() / 2, heart_image.get_height() / 2),
#                           (heart_image.get_width(), heart_image.get_height()),
#                           ((i + 1) * 50, 100), (50, 50))
