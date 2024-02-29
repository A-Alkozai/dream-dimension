import SimpleGUICS2Pygame.simpleguics2pygame
from vector import Vector
from entity import Entity


class Floor(Entity):
    def __init__(self, start, end, border, colour):
        super().__init__()

        self.start = Vector(start[0], start[1])
        self.end = Vector(end[0], end[1])
        self.border = border
        self.thickness = 2*border+1
        self.colour = colour

    def draw(self, canvas):
        canvas.draw_line(self.start.get_p(),
                         self.end.get_p(),
                         self.thickness,
                         self.colour)

    def update(self):
        pass
