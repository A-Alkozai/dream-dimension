from state import State


class Projectile(State):
    def __init__(self, name, damage=50, **kwargs):
        super().__init__(name, **kwargs)

        self.name = name
        self.GRAVITY = False
        self.IDLE = False
        self.DEAD = False

        self.is_right = True
        self.is_red = True
        self.is_friendly = True
        self.damage = damage

    def update(self):
        self.set_direction(self.is_right)
        self.frame_update()
        self.movement()
        self.velocity.y = 0
        self.position.add(self.velocity)
        self.boundaries()
        self.velocity.multiply(0.85)

    def frame_update(self):
        # Choose correct row
        self.frame_index[1] = 1
        if self.is_red:
            self.frame_index[1] = 0

        if self.frame_count % 3 == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % 15
        self.frame_count += 1

    def set_direction(self, is_right):
        self.RIGHT = False
        self.LEFT = True
        self.rotation = 3
        if is_right:
            self.RIGHT = True
            self.LEFT = False
            self.rotation = 0

    def boundaries(self):
        if self.position.x <= 0 or self.position.x >= 1920 or self.position.y <= 0 or self.position.y >= 1080:
            self.DEAD = True
