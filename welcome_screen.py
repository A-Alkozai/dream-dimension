import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class WelcomeScreen:
    def __init__(self, canvas_width, canvas_height):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.show_welcome_screen = True
        self.click_to_start = True

        # Load welcome image
        self.welcome_image = simplegui.load_image('welcome_msg.png')
        print("Welcome image dimensions:", self.welcome_image.get_width(), "x", self.welcome_image.get_height())

        # Load description images
        self.description_images = [simplegui.load_image(f'desc{i}.png') for i in range(1, 4)]
        for i, desc_image in enumerate(self.description_images):
            print(f"Description image {i+1} dimensions:", desc_image.get_width(), "x", desc_image.get_height())

        # Load click image
        self.click_image = simplegui.load_image('click.png')
        print("Click image dimensions:", self.click_image.get_width(), "x", self.click_image.get_height())

        # Load muffin image
        self.muffin_image = simplegui.load_image('muffin.png')
        print("Muffin image dimensions:", self.muffin_image.get_width(), "x", self.muffin_image.get_height())

    def draw(self, canvas):
        if self.show_welcome_screen:
            # Draw welcome image
            canvas.draw_image(self.welcome_image, (self.canvas_width / 2, self.canvas_height / 2), (self.canvas_width, self.canvas_height), (self.canvas_width / 2, self.canvas_height / 2), (self.canvas_width, self.canvas_height))

            # Draw description images
            desc_image_size = (400, 200)  # Adjust the size of description images as needed
            for i, desc_image in enumerate(self.description_images):
                canvas.draw_image(desc_image, (desc_image.get_width() / 2, desc_image.get_height() / 2), (desc_image.get_width(), desc_image.get_height()), (self.canvas_width / 2, 200 + (i * 220)), desc_image_size)

            # Draw click image
            canvas.draw_image(self.click_image, (self.click_image.get_width() / 2, self.click_image.get_height() / 2), (self.click_image.get_width(), self.click_image.get_height()), (self.canvas_width / 2, 500), (self.click_image.get_width(), self.click_image.get_height()))

            # Draw muffin images
            canvas.draw_image(self.muffin_image, (50, 50), (100, 100), (150, self.canvas_height - 100), (100, 100))
            canvas.draw_image(self.muffin_image, (50, 50), (100, 100), (self.canvas_width - 150, self.canvas_height - 100), (100, 100))

    def start_game(self):
        self.show_welcome_screen = False

    def reset_game(self):
        self.show_welcome_screen = True
        # Reset lives and score here



