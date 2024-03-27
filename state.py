import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import Vector
from entity import Entity


class State(Entity):
    def __init__(self, walk_frames=0, jump_frames=0, attack_frames=0, dmg_frames=0, health_max=100, mana_max=120,
                 mana_recharge_rate=5, gravity_strength=1.5, player=None, projectile=None, interaction=None, speed=1,
                 **kwargs):

        # different states
        self.GRAVITY = True
        self.IDLE = True
        self.PATROL = False
        self.JUMP = False
        self.FALL = False
        self.LEFT = False
        self.RIGHT = False
        self.ATTACK1 = False
        self.ATTACK1_END = True
        self.ATTACK1_COOLDOWN = False
        self.ATTACK2 = False
        self.SHOOTING = False
        self.HURT = False
        self.HIT = False
        self.DIE = False
        self.DEAD = False

        # patrol conditions
        self.patrol_right = True
        self.patrolled_distance = 0
        self.max_patrol_distance = 250

        # number of frames per state
        self.walk_frame = walk_frames
        self.jump_frame = jump_frames
        self.attack_frame = attack_frames
        self.dmg_frame = dmg_frames

        # default idle frame
        self.idle_frame = [0, 0]
        self.fps = 3

        # player & projectile object
        self.player = player
        self.interaction = interaction

        self.projectile = projectile
        self.count = 0

        # general & gravity speed
        self.speed = speed
        self.weight = gravity_strength

        # health attributes
        self.health = health_max
        self.health_max = health_max
        self.damaged = 0

        # mana attributes
        self.mana = mana_max
        self.mana_max = mana_max
        self.mana_recharge_rate = mana_recharge_rate
        self.mana_recharge_timer = simplegui.create_timer(1000, self.recharge_mana)

        super().__init__(**kwargs)

    def state_update(self):
        if self.damaged > 0:
            self.HURT = True
            self.health -= self.damaged
            self.damaged = 0

    def update(self):
        # Update state before updating frame
        self.state_update()
        self.frame_update()
        self.movement()
        # Add all movements
        self.position.add(self.velocity)
        # Ensure entity not below floor
        # self.position.y = min(self.position.y, 900 - self.frame_centre_y)
        self.velocity.multiply(0.80)

    def movement(self):
        speed = self.speed
        # If jumping, then no gravity occurs (vice versa)
        if self.JUMP:
            self.velocity += Vector(0, -5) * self.speed
        elif self.GRAVITY:
            self.velocity.y += self.weight

        # Patrol movements
        if self.PATROL:
            self.ATTACK1 = False
            self.ATTACK1_END = True
            self.speed *= 0.5
            if self.patrol_right:
                self.RIGHT = True
                self.LEFT = False
            else:
                self.RIGHT = False
                self.LEFT = True
            self.patrolled_distance += abs(self.velocity.x)
            if self.patrolled_distance >= self.max_patrol_distance:
                self.patrol_right = not self.patrol_right
                self.patrolled_distance = 0

        # Move left and right
        if self.RIGHT:
            self.velocity += Vector(1, 0) * self.speed
            self.idle_frame = [0, 0]
        if self.LEFT:
            self.velocity += Vector(-1, 0) * self.speed
            self.idle_frame = [2, 0]
        self.speed = speed

    def frame_update(self):
        if self.ATTACK1_COOLDOWN:
            self.count += 1
            if self.count == 30:
                self.ATTACK1_COOLDOWN = False
                self.count = 0

        if self.HURT:
            # Enable/Disable some states when hurt
            self.LEFT, self.RIGHT, self.ATTACK1, self.ATTACK2 = False, False, False, False
            self.JUMP, self.PATROL = False, False
            self.ATTACK1_END = True

            # Choosing correct frame
            self.frame_index = [3, 0]
            if self.idle_frame[0] == 0:
                self.frame_index = [1, 0]

            # Control duration
            if self.frame_count > 0:
                self.frame_count = -5

            # Turn hurt off
            if self.frame_count % 6 == 0:
                self.HURT = False

        # Launch attack mid-air
        elif self.ATTACK1 and (self.JUMP or self.FALL):
            # Stops left/right movement during attack
            self.RIGHT, self.LEFT, self.ATTACK2 = False, False, False
            self.ATTACK1_END = False

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

            # Ensures player falls during midair attack
            if self.frame_count % 8 == 0:
                self.JUMP = False
                self.FALL = True

            # Control FPS of animation
            if self.frame_count % 4 == 0:
                self.frame_index[0] = (self.frame_index[0] + 1) % self.attack_frame
                if self.frame_index[0] == 0:
                    self.ATTACK1 = False
                    self.ATTACK1_END = True

        elif self.ATTACK2 and self.ATTACK1_END:
            self.RIGHT, self.LEFT, self.JUMP, self.ATTACK1 = False, False, False, False
            # Choosing correct row
            if self.idle_frame[0] == 0:
                self.frame_index[1] = 9
            elif self.frame_index[1] != 10:
                self.frame_index = [0, 10]

            # Reset count so animation is always played the same
            if self.frame_count > 0:
                self.frame_count = -6

            # Control FPS
            if self.frame_count % 7 == 0:
                self.frame_index[0] = (self.frame_index[0] + 1) % self.attack_frame

                # Create projectile at 4th frame
                if self.frame_index[0] == 3:
                    self.SHOOTING = True
                    self.shoot()

                # Turns off animation at last frame
                if self.frame_index[0] == 0:
                    self.ATTACK2 = False

        elif self.ATTACK1:
            if not self.ATTACK1_COOLDOWN:
                # Stops left/right movement during attack
                self.RIGHT, self.LEFT, self.ATTACK2 = False, False, False
                self.ATTACK1_END = False

                # Choosing correct row
                if self.idle_frame[0] == 0:
                    self.frame_index[1] = 5
                elif self.frame_index[1] != 6:
                    self.frame_index = [0, 6]

                # Ensuring the column number is not greater than number of frames in the row
                if self.frame_index[0] >= self.attack_frame:
                    self.frame_index[0] = 0

                # Ensures attack occurs
                if self.frame_index[0] == 1:
                    self.HIT = True
                else:
                    self.HIT = False

                # Reset count so animation is always played the same
                if self.frame_count > 0:
                    self.frame_count = -self.fps + 1

                # Control FPS
                if self.frame_count % self.fps == 0:
                    self.frame_index[0] = (self.frame_index[0] + 1) % self.attack_frame

                    # Create projectile at 4th frame
                    if self.frame_index[0] == 3 and self.player is not None:
                        self.SHOOTING = True
                        self.shoot()

                    # Turns off animation at last frame
                    if self.frame_index[0] == 0:
                        self.ATTACK1 = False
                        self.ATTACK1_END = True
                        self.ATTACK1_COOLDOWN = True

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
            self.frame_index[0] = self.idle_frame[0]
            self.frame_index[1] = self.idle_frame[1]
        self.frame_count += 1

    def shoot(self):
        pass

    def start_mana_recharge(self):
        self.mana_recharge_timer.start()

    def stop_mana_recharge(self):
        if self.mana >= self.mana_max:
            self.mana_recharge_timer.stop()

    def recharge_mana(self):
        self.mana = min(self.mana + self.mana_recharge_rate, self.mana_max)
        self.stop_mana_recharge()
