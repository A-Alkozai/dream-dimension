import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


# Class to represent a health bar
class HealthBar:
    def __init__(self, max_health, position, dimensions, color):
        # Initialize health bar attributes
        self.max_health = max_health  # Maximum health value
        self.current_health = max_health  # Current health value
        self.position = position  # Position of the health bar
        self.dimensions = dimensions  # Dimensions of the health bar
        self.color = color  # Color of the health bar

    # Method to draw the health bar on the canvas
    def draw(self, canvas):
        # Calculate the width of the health bar based on current health
        bar_width = self.dimensions[0] * (self.current_health / self.max_health)
        # Draw the health bar on the canvas
        canvas.draw_polygon([(self.position[0], self.position[1]),
                             (self.position[0] + bar_width, self.position[1]),
                             (self.position[0] + bar_width, self.position[1] + self.dimensions[1]),
                             (self.position[0], self.position[1] + self.dimensions[1])],
                            2, self.color, self.color)

    # Method to update the current health value
    def update(self, new_health):
        # Ensure new health value is within bounds
        self.current_health = min(max(new_health, 0), self.max_health)


# Draw handler function for the frame
def draw(canvas):
    global health_bar

    # Draw the health bar on the canvas
    health_bar.draw(canvas)


# Function to reduce health when "Reduce Health" button is clicked
def reduce_health():
    global health_bar
    # Reduce health by 10 units
    health_bar.update(health_bar.current_health - 10)


# Function to simulate "suicide" by setting health to 0 when "Suicide" button is clicked
def suicide():
    global health_bar
    # Set health to 0
    health_bar.update(0)
    # Placeholder for game restart or other actions
    print("Game restarted!")  # Placeholder for game restart code


# Function to kill the game when "Kill Game" button is clicked
def kill_game():
    # Placeholder for game termination actions
    print("Game killed!")  # Placeholder for game kill actions


# Initialize health bar with maximum health of 100
health_bar = HealthBar(100, (50, 50), (200, 20), "red")

# Create a frame
frame = simplegui.create_frame("Health Bar Example", 300, 200)
frame.set_draw_handler(draw)

# Add buttons to the frame
frame.add_button("Reduce Health", reduce_health)
frame.add_button("Suicide", suicide)
frame.add_button("Kill Game", kill_game)

# Start the frame
frame.start()
