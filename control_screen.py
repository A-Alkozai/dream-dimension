from entity import Entity
from vector import Vector


class Background(Entity):
    def __init__(self, canvas_width, canvas_height, img_url):
        super().__init__(position=Vector(canvas_width/2, canvas_height/2), img_url=img_url, img_dest_dim=(canvas_width, canvas_height))


class ControlScreen:
    def __init__(self, welcome_screen):
        self.canvas_width = welcome_screen.canvas_width
        self.canvas_height = welcome_screen.canvas_height
        self.welcome_screen = welcome_screen
        self.show_controls_screen = False

        # Creating background and back_button
        self.background_entity = Background(self.canvas_width, self.canvas_height, "images/background.png")
        self.back_button = Entity(kind='button', position=Vector(200, 1000), img_url="images/buttons/back.png",
                                  img_dest_dim=(286 * 1.3, 140 * 1.3))

    def draw(self, canvas):
        if self.show_controls_screen:
            # Draw background
            self.background_entity.draw(canvas)

            # Draw controls title
            controls = Entity(kind='text', position=Vector(self.canvas_width/2, 200), img_url="images/buttons/controls.png", img_dest_dim=(346*1.2, 81*1.2))
            controls.draw(canvas)

            # Draw controls text
            controls_text = Entity(kind='text', position=Vector(self.canvas_width / 2, 500), img_url="images/texts/controls.png", img_dest_dim=(1169, 519))
            controls_text.draw(canvas)

            # Draw back button
            self.back_button.draw(canvas)

    def show_controls(self):
        self.show_controls_screen = True

    def go_back(self):
        self.show_controls_screen = False
        self.welcome_screen.show_welcome_screen = True
        self.welcome_screen.credits_shown = False
