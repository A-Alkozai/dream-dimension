try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Global variables
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 150
STAMINA_MAX = 100
STAMINA_REGEN_RATE = 1.0  # Increase regeneration rate
STAMINA_DASH_COST = 30
STAMINA_DASH_COUNT = 3

stamina = STAMINA_MAX
dashes_left = STAMINA_DASH_COUNT

# Timer handler for stamina regeneration
def regen_stamina():
    global stamina
    if stamina < STAMINA_MAX:
        stamina += STAMINA_REGEN_RATE
        if stamina > STAMINA_MAX:
            stamina = STAMINA_MAX

# Timer for stamina regeneration
timer = simplegui.create_timer(300, regen_stamina)  # Decrease timer interval for faster regeneration

# Handler for dash action
def dash():
    global stamina, dashes_left
    if dashes_left > 0 and stamina >= STAMINA_DASH_COST:
        stamina -= STAMINA_DASH_COST
        dashes_left -= 1

# Handler for resetting dashes
def reset_dashes():
    global dashes_left
    dashes_left = STAMINA_DASH_COUNT

# Handler for drawing on the canvas
def draw(canvas):
    # Draw background
    canvas.draw_polygon([(0, 0), (CANVAS_WIDTH, 0), (CANVAS_WIDTH, CANVAS_HEIGHT), (0, CANVAS_HEIGHT)], 10, 'Black')
    
    # Draw stamina bar
    bar_width = stamina / STAMINA_MAX * (CANVAS_WIDTH - 20)
    canvas.draw_line((10, 100), (bar_width + 10, 100), 10, "Green")
    canvas.draw_line((bar_width + 10, 100), (CANVAS_WIDTH - 10, 100), 10, "Red")
    canvas.draw_text("Stamina:", [10, 125], 20, "White")
    canvas.draw_text(str(round(stamina)), [100, 125], 20, "White")
    
    # Draw dashes left
    canvas.draw_text("Dashes left: " + str(dashes_left), [10, 144], 20, "White")

# Create frame and register event handlers
frame = simplegui.create_frame("Stamina Bar", CANVAS_WIDTH, CANVAS_HEIGHT)

frame.set_draw_handler(draw)
frame.add_button("Dash", dash, 100)

frame.add_button("Reset Dashes", reset_dashes, 100)

# Start timers
timer.start()
frame.start()
