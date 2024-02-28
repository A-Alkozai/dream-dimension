import simplegui

class HealthBar:
    def __init__(self, max_health, position, dimensions, color):
        self.max_health = max_health
        self.current_health = max_health
        self.position = position
        self.dimensions = dimensions
        self.color = color

    def draw(self, canvas):
        bar_width = self.dimensions[0] * (self.current_health / self.max_health)
        canvas.draw_polygon([(self.position[0], self.position[1]),
                             (self.position[0] + bar_width, self.position[1]),
                             (self.position[0] + bar_width, self.position[1] + self.dimensions[1]),
                             (self.position[0], self.position[1] + self.dimensions[1])],
                            2, self.color, self.color)

    def update(self, new_health):
        self.current_health = min(max(new_health, 0), self.max_health)

# Test health bar
def draw(canvas):
    global health_bar
    health_bar.draw(canvas)

def reduce_health():
    global health_bar
    health_bar.update(health_bar.current_health - 10)

# Initialize health bar
health_bar = HealthBar(100, (50, 50), (200, 20), "red")

# Create a frame
frame = simplegui.create_frame("Health Bar Example", 300, 200)
frame.set_draw_handler(draw)

# Add a button to reduce health
frame.add_button("Reduce Health", reduce_health)

# Start the frame
frame.start()
