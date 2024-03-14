from vector import Vector
from entity import Entity

class State(Entity):
    def __init__(self, walk, jump, attack, dmg,
                 gravity_strength=2, player=None, speed=1, **kwargs):

        self.GRAVITY = True
        self.IDLE = True
        self.JUMP = False
        self.LEFT = False
        self.RIGHT = False
        self.ATTACK = False
        self.DAMAGE = False

        self.walk_frame = walk
        self.jump_frame = jump
        self.attack_frame = attack
        self.dmg_frame = dmg

        self.idle_frame = [0, 0]
        self.weight = gravity_strength
        self.player = player
        self.speed = speed

        super().__init__(**kwargs)

    def draw(self, canvas):
        frame_centre = (self.frame_width * self.frame_index[0] + self.frame_centre_x,
                        self.frame_height * self.frame_index[1] + self.frame_centre_y)

        canvas.draw_image(self.img,
                          frame_centre,
                          self.img_dim,
                          self.position.get_p(),
                          self.img_dest_dim,
                          self.rotation)
        self.update()

    def state_update(self):
        if self.player.position.x-50 > self.position.x:
            self.RIGHT = True
            self.LEFT = False
            self.ATTACK = False
        elif self.player.position.x+50 < self.position.x:
            self.LEFT = True
            self.RIGHT = False
            self.ATTACK = False
        elif self.player.position.x+50 > self.position.x or self.player.position.x-50 < self.position.x:
            self.LEFT = False
            self.RIGHT = False
            self.ATTACK = True
        else:
            self.LEFT = False
            self.RIGHT = False
            self.ATTACK = False
        # if statements toggling the states for enemies

    def update(self):
        self.state_update()
        self.frame_update()
        self.movement()
        self.position.add(self.velocity)
        self.position.y = min(self.position.y, 900 - self.frame_centre_y)
        self.velocity.multiply(0.85)

    def movement(self):
        if self.JUMP:
            self.velocity += Vector(0, -5) * self.speed
        if self.RIGHT:
            self.velocity += Vector(1, 0) * self.speed
        elif self.LEFT:
            self.velocity += Vector(-1, 0) * self.speed
        if self.GRAVITY:
            self.velocity.y += self.weight

    def frame_update(self):
        if self.DAMAGE:
            self.frame_index[1] = 0
            if self.idle_frame == [0, 0]:
                self.frame_index[0] = 1
            else:
                self.frame_index[0] = 3
            if self.frame_count % 5 == 0:
                self.DAMAGE = False

        elif self.ATTACK and self.JUMP:
            if self.idle_frame == [0, 0]:
                self.frame_index[1] = 7
            else:
                self.frame_index[1] = 8
            if self.frame_index[0] >= self.attack_frame:
                self.frame_index[0] = 0
            self.frame_index[0] = (self.frame_index[0] + 1) % self.attack_frame

        elif self.ATTACK:
            if self.idle_frame == [0, 0]:
                self.frame_index[1] = 5
            else:
                self.frame_index[1] = 6
            if self.frame_index[0] >= self.attack_frame:
                self.frame_index[0] = 0
            if self.frame_count % self.attack_frame == 0:
                self.frame_index[0] = (self.frame_index[0] + 1) % self.attack_frame
                if self.frame_index[0] == 0:
                    self.ATTACK = False

        elif self.JUMP:
            if self.idle_frame == [0, 0]:
                self.frame_index[1] = 3
            else:
                self.frame_index[1] = 4
            if self.frame_index[0] >= self.jump_frame:
                self.frame_index[0] = 0
            if self.frame_count % 10 == 0:
                self.frame_index[0] = (self.frame_index[0] + 1) % self.jump_frame
                if self.frame_index[0] == 0:
                    self.JUMP = False

        elif self.RIGHT:
            self.frame_index[1] = 1
            if self.frame_index[0] >= self.walk_frame:
                self.frame_index[0] = 0
            if self.frame_count % self.walk_frame == 0:
                self.frame_index[0] = (self.frame_index[0] + 1) % self.walk_frame
                self.idle_frame = [0, 0]

        elif self.LEFT:
            self.frame_index[1] = 2
            if self.frame_index[0] >= self.walk_frame:
                self.frame_index[0] = 0
            if self.frame_count % self.walk_frame == 0:
                self.frame_index[0] = (self.frame_index[0] + 1) % self.walk_frame
                self.idle_frame = [2, 0]

        else:
            self.frame_index[0] = self.idle_frame[0]
            self.frame_index[1] = self.idle_frame[1]
        self.frame_count += 1


