from entity import Entity
from vector import Vector


class Background(Entity):
    def __init__(self, canvas_width, canvas_height, img_url):
        super().__init__(position=Vector(canvas_width / 2, canvas_height / 2), img_url=img_url,
                         img_dest_dim=(canvas_width, canvas_height))


class StoryScreen:
    def __init__(self, welcome_screen):
        self.canvas_width = welcome_screen.canvas_width
        self.canvas_height = welcome_screen.canvas_height
        self.welcome_screen = welcome_screen
        self.show_story_screen = False

        self.screen1 = True
        self.screen2 = False
        self.screen3 = False

        # Creating background and buttons
        self.background_entity = Background(self.canvas_width, self.canvas_height, "images/main_menu_bg.jpg")
        self.choice1 = Entity(kind='button', position=Vector(self.canvas_width/2, 700), img_url="images/buttons/choice1.png",
                              img_dest_dim=(775 * 1, 78 * 1))
        self.choice2 = Entity(kind='button', position=Vector(self.canvas_width/2, 700), img_url="images/buttons/choice2.png",
                              img_dest_dim=(711 * 1, 65 * 1))
        self.choice3 = Entity(kind='button', position=Vector(self.canvas_width/2, 700), img_url="images/buttons/choice3.png",
                              img_dest_dim=(137 * 1.6, 55 * 1.6))

        # Creating story text
        self.story1 = Entity(kind='text', position=Vector(self.canvas_width/2, 400), img_url="images/texts/story1.png",
                             img_dest_dim=(1089 * 1.15, 124 * 1.15))
        self.story2 = Entity(kind='text', position=Vector(self.canvas_width / 2, 400), img_url="images/texts/story2.png",
                             img_dest_dim=(1197 * 1.15, 57 * 1.15))
        self.story3 = Entity(kind='text', position=Vector(self.canvas_width / 2, 400), img_url="images/texts/story3.png",
                             img_dest_dim=(942 * 1.15, 311 * 1.15))

    def draw(self, canvas):
        if self.show_story_screen:
            # Draw background
            self.background_entity.draw(canvas)

            # Draw story text + button
            if self.screen1:
                self.story1.draw(canvas)
                self.choice1.draw(canvas)

            elif self.screen2:
                self.story2.draw(canvas)
                self.choice2.draw(canvas)

            elif self.screen3:
                self.story3.draw(canvas)
                self.choice3.draw(canvas)

    def show_story(self):
        self.show_story_screen = True

    def hide_story(self):
        self.show_story_screen = False
        self.screen1 = True
        self.screen2, self.screen3 = False, False
