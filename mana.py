import simplegui

# Class to represent a ManaBar
class ManaBar:
    def __init__(self, max_mana, position, width, height, color, decrease_rate, recharge_rate):
        self.max_mana = max_mana
        self.current_mana = max_mana
        self.position = position
        self.width = width
        self.height = height
        self.color = color
        self.decrease_rate = decrease_rate
        self.recharge_rate = recharge_rate

        # Create a timer to decrease 'mana'
        self.decrease_timer = simplegui.create_timer(1000, self.decrease_mana)
        # Create a timer to recharge 'mana'
        self.recharge_timer = simplegui.create_timer(1000, self.recharge_mana)

        # Flag to track if any movement key is pressed
        self.is_movement_key_pressed = False

    # Method to draw the mana bar on the canvas
    def draw(self, canvas):
        # Calculate the width of the mana bar based on current mana
        bar_width = self.width * (self.current_mana / self.max_mana)
        # Draw the mana bar on the canvas
        canvas.draw_polygon([(self.position[0], self.position[1]),
                             (self.position[0] + bar_width, self.position[1]),
                             (self.position[0] + bar_width, self.position[1] + self.height),
                             (self.position[0], self.position[1] + self.height)],
                            2, self.color, self.color)

    # Method to start the timer for decreasing mana
    def start_decrease_timer(self):
        self.decrease_timer.start()

    # Method to stop the timer for decreasing mana
    def stop_decrease_timer(self):
        self.decrease_timer.stop()

    # Method to decrease the mana
    def decrease_mana(self):
        if self.is_movement_key_pressed:
            self.current_mana = max(self.current_mana - self.decrease_rate, 0)

    # Method to start the timer for recharging mana
    def start_recharge_timer(self):
        self.recharge_timer.start()

    # Method to stop the timer for recharging mana
    def stop_recharge_timer(self):
        self.recharge_timer.stop()

    # Method to recharge the mana
    def recharge_mana(self):
        self.current_mana = min(self.current_mana + self.recharge_rate, self.max_mana)

    # Method to handle key down events
    def key_down(self, key):
        # Start the decrease timer if a movement key is pressed
        if key in (simplegui.KEY_MAP["w"], simplegui.KEY_MAP["a"], simplegui.KEY_MAP["s"], simplegui.KEY_MAP["d"]):
            self.is_movement_key_pressed = True
            self.start_decrease_timer()
            self.stop_recharge_timer()

    # Method to handle key up events
    def key_up(self, key):
        # Stop the decrease timer if no movement keys are pressed
        if key in (simplegui.KEY_MAP["w"], simplegui.KEY_MAP["a"], simplegui.KEY_MAP["s"], simplegui.KEY_MAP["d"]):
            self.is_movement_key_pressed = False
            self.stop_decrease_timer()
            self.start_recharge_timer()


# Draw handler function for the frame
def draw(canvas):
    global mana_bar

    # Draw the mana bar on the canvas
    mana_bar.draw(canvas)


# Create a frame
frame = simplegui.create_frame("Mana Bar Example", 300, 200)
frame.set_draw_handler(draw)

# Initialize mana bar with maximum mana of 100
mana_bar = ManaBar(100, (10, 10), 200, 20, "blue", decrease_rate=1, recharge_rate=1)

# Set key down and key up handlers
frame.set_keydown_handler(mana_bar.key_down)
frame.set_keyup_handler(mana_bar.key_up)

# Start the frame
frame.start()
