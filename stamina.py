import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


# Class to represent a StaminaBar
class StaminaBar:
    def __init__(self, max_stamina, position, width, height, color, decrease_rate):
        # Initialize stamina bar attributes
        self.max_stamina = max_stamina  # Maximum stamina value
        self.current_stamina = max_stamina  # Current stamina value
        self.position = position  # Position of the stamina bar
        self.width = width  # Width of the stamina bar
        self.height = height  # Height of the stamina bar
        self.color = color  # Color of the stamina bar
        self.decrease_rate = decrease_rate  # Rate at which stamina decreases (per second)

        # Create a timer to decrease stamina
        self.timer = simplegui.create_timer(1000, self.decrease_stamina)

        # Flag to track if any movement key is pressed
        self.is_movement_key_pressed = False

    # Method to draw the stamina bar on the canvas
    def draw(self, canvas):
        # Calculate the width of the stamina bar based on current stamina
        bar_width = self.width * (self.current_stamina / self.max_stamina)
        # Draw the stamina bar on the canvas
        canvas.draw_polygon([(self.position[0], self.position[1]),
                             (self.position[0] + bar_width, self.position[1]),
                             (self.position[0] + bar_width, self.position[1] + self.height),
                             (self.position[0], self.position[1] + self.height)],
                            2, self.color, self.color)

    # Method to start the timer for decreasing stamina
    def start_timer(self):
        self.timer.start()

    # Method to stop the timer for decreasing stamina
    def stop_timer(self):
        self.timer.stop()

    # Method to decrease the stamina
    def decrease_stamina(self):
        if self.is_movement_key_pressed:
            self.current_stamina = max(self.current_stamina - self.decrease_rate, 0)

    # Method to handle key down events
    def key_down(self, key):
        # Start the timer if a movement key is pressed
        if key in (simplegui.KEY_MAP["w"], simplegui.KEY_MAP["a"], simplegui.KEY_MAP["s"], simplegui.KEY_MAP["d"]):
            self.is_movement_key_pressed = True
            self.start_timer()

    # Method to handle key up events
    def key_up(self, key):
        # Stop the timer if no movement keys are pressed
        if key in (simplegui.KEY_MAP["w"], simplegui.KEY_MAP["a"], simplegui.KEY_MAP["s"], simplegui.KEY_MAP["d"]):
            self.is_movement_key_pressed = False
            self.stop_timer()


# Draw handler function for the frame
def draw(canvas):
    global stamina_bar

    # Draw the stamina bar on the canvas
    stamina_bar.draw(canvas)


# Create a frame
frame = simplegui.create_frame("Stamina Bar Example", 300, 200)
frame.set_draw_handler(draw)

# Initialize stamina bar with maximum stamina of 100
stamina_bar = StaminaBar(100, (50, 50), 200, 20, "blue", decrease_rate=1)

# Set key down and key up handlers
frame.set_keydown_handler(stamina_bar.key_down)
frame.set_keyup_handler(stamina_bar.key_up)

# Start the frame
frame.start()
