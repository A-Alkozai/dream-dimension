import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from entity import Entity


class State(Entity):
    def __init__(self, walk, jump, attack, dmg,
                 gravity_strength=1.5, player=None, speed=1, **kwargs):

        # different states
        self.GRAVITY = True
        self.IDLE = True
        self.JUMP = False
        self.FALL = False
        self.LEFT = False
        self.RIGHT = False
        self.ATTACK = False
        self.DAMAGE = False

        # number of frames per state
        self.walk_frame = walk
        self.jump_frame = jump
        self.attack_frame = attack
        self.dmg_frame = dmg

        self.idle_frame = [0, 0]
        self.weight = gravity_strength

        # player object
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
        # If enemy is far from player, move towards player position
        if self.player.position.x-25 > self.position.x:
            self.RIGHT = True
            self.LEFT = False
            self.ATTACK = False
        elif self.player.position.x+25 < self.position.x:
            self.LEFT = True
            self.RIGHT = False
            self.ATTACK = False
        # If enemy is close to player, enemy attacks
        elif self.player.position.x+25 > self.position.x or self.player.position.x-25 < self.position.x:
            self.LEFT = False
            self.RIGHT = False
            self.ATTACK = True
        # Enemy idle state
        else:
            self.LEFT = False
            self.RIGHT = False
            self.ATTACK = False

    def update(self):
        # Update state before updating frame
        self.state_update()
        self.frame_update()
        self.movement()
        # Add all movements
        self.position.add(self.velocity)
        # Ensure entity not below floor
        self.position.y = min(self.position.y, 900 - self.frame_centre_y)
        self.velocity.multiply(0.85)

    def movement(self):
        if self.JUMP:
            self.velocity += Vector(0, -5) * self.speed
        elif self.GRAVITY:
            self.velocity.y += self.weight
        if self.RIGHT:
            self.velocity += Vector(1, 0) * self.speed
            self.idle_frame = [0, 0]
        if self.LEFT:
            self.velocity += Vector(-1, 0) * self.speed
            self.idle_frame = [2, 0]

    def frame_update(self):
        if self.DAMAGE:
            pass

        # Launch attack mid-air
        elif self.ATTACK and (self.JUMP or self.FALL):
            # Choosing correct row
            self.frame_index[1] = 8
            if self.idle_frame == [0, 0]:
                self.frame_index[1] = 7

            # Ensuring the column number is not greater than number of frames in the row
            if self.frame_index[0] >= self.attack_frame:
                self.frame_index[0] = 0

            # Reset count so animation is always played the same
            if self.frame_count > 0:
                self.frame_count = -7

            # Ensures player falls during mid-air attack
            if self.frame_count % 8 == 0:
                self.JUMP = False
                self.FALL = True
            # Control FPS of animation
            if self.frame_count % 4 == 0:
                self.frame_index[0] = (self.frame_index[0] + 1) % self.attack_frame
                if self.frame_index[0] == 0:
                    self.ATTACK = False

        elif self.ATTACK:
            # Stops left/right movement during attack
            self.RIGHT, self.LEFT = False, False

            # Choosing correct row
            if self.idle_frame[0] == 0:
                self.frame_index[1] = 5
            elif self.frame_index[1] != 6:
                self.frame_index = [0, 6]

            # Ensuring the column number is not greater than number of frames in the row
            if self.frame_index[0] >= self.attack_frame:
                self.frame_index[0] = 0

            # Reset count so animation is always played the same
            if self.frame_count > 0:
                self.frame_count = -2

            # Control FPS
            if self.frame_count % 3 == 0:
                self.frame_index[0] = (self.frame_index[0] + 1) % self.attack_frame
                # Turns off animation at last frame
                if self.frame_index[0] == 0:
                    self.ATTACK = False

        elif self.JUMP:
            # Choosing correct row
            self.frame_index = [0, 4]
            if self.idle_frame == [0, 0]:
                self.frame_index = [0, 3]

            # Reset count so animation is always played the same
            if self.frame_count > 0:
                self.frame_count = -7

            # Control FPS and turns off animation
            if self.frame_count % 8 == 0:
                self.JUMP = False
                self.FALL = True

        elif self.FALL:
            # Choosing correct row
            self.frame_index = [1, 4]
            if self.idle_frame == [0, 0]:
                self.frame_index = [1, 3]

            # Fall animation until touches ground
            if self.position.y == 900 - self.frame_centre_y:
                self.FALL = False

        elif self.RIGHT and not self.LEFT:
            # Choosing correct row
            self.frame_index[1] = 1
            if self.frame_index[0] >= self.walk_frame:
                self.frame_index[0] = 0

            # Control FPS
            if self.frame_count % self.walk_frame == 0:
                self.frame_index[0] = (self.frame_index[0] + 1) % self.walk_frame

        elif self.LEFT and not self.RIGHT:
            # Choosing correct row
            self.frame_index[1] = 2
            if self.frame_index[0] >= self.walk_frame:
                self.frame_index[0] = 0

            # Control FPS
            if self.frame_count % self.walk_frame == 0:
                self.frame_index[0] = (self.frame_index[0] + 1) % self.walk_frame

        else:
            # Set idle frame
            self.frame_index[0] = self.idle_frame[0]
            self.frame_index[1] = self.idle_frame[1]
        self.frame_count += 1


