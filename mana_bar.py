# Class to represent a ManaBar
class ManaBar:
    def __init__(self, game_manager):
        self.position = (10, 95)
        self.outline_position = (10, 95)
        self.width = 200
        self.height = 20
        self.color = 'blue'

        self.game_manager = game_manager

        self.max_mana = 100
        self.current_mana = self.max_mana

    # Method to draw the mana bar on the canvas
    def draw(self, canvas):
        self.current_mana = self.game_manager.player.mana
        # Calculate the width of the mana bar based on current mana
        bar_width = self.width * (self.current_mana / self.max_mana)
        # Draw mana bar outline
        canvas.draw_polygon([(self.outline_position[0] - 5, self.outline_position[1] - 5),
                             (self.outline_position[0] + 240 + 5, self.outline_position[1] - 5),
                             (self.outline_position[0] + 240 + 5, self.outline_position[1] + 20 + 5),
                             (self.outline_position[0] - 5, self.outline_position[1] + 20 + 5)],
                            2, "Black", "Black")

        # Draw the mana bar on the canvas
        canvas.draw_polygon([(self.position[0], self.position[1]),
                             (self.position[0] + bar_width, self.position[1]),
                             (self.position[0] + bar_width, self.position[1] + self.height),
                             (self.position[0], self.position[1] + self.height)],
                              2, self.color, self.color)

        # Draw outline bars
        canvas.draw_line((self.outline_position[0] + 80, self.outline_position[1] - 5),
                         (self.outline_position[0] + 80, self.outline_position[1] + 20 + 5), 5, "Black")
        canvas.draw_line((self.outline_position[0] + 160, self.outline_position[1] - 5),
                         (self.outline_position[0] + 160, self.outline_position[1] + 20 + 5), 5, "Black")
