import simplegui

# Initialize globals
WIDTH = 400
HEIGHT = 100
score = 0
MAX_SCORE = 100

# Handler to draw on canvas
def draw(canvas):
    global score
    
    canvas.draw_text("Score: " + str(score), (10, 30), 24, 'White')

# Handler to increase score
def increase_score():
    global score
    if score < MAX_SCORE:
        score += 1

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Score Bar", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.add_button("Increase Score", increase_score)

# Start the frame animation
frame.start()
