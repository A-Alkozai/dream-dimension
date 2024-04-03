from projectile import Projectile
from vector import Vector
from state import State
from entity import Entity
import math


class Enemy(Entity):
    def __init__(self, walk_frames=0, jump_frames=0, attack_frames=0, flinch_frames=0, is_ranged=True, mana_max=40,
                 mana_recharge_rate=1, cooldown=30, speed=1, health=1, damage=1, points=1, **kwargs):
        super().__init__(**kwargs)

        # Number of frames per animation type
        self.walk_frames = walk_frames
        self.jump_frames = jump_frames
        self.attack_frames = attack_frames
        self.flinch_frames = flinch_frames

        self.state = State()
        self.state.PATROL = True
        self.idle_frame = [0, 0]

        # patrol conditions
        self.patrol_right = True
        self.patrolled_distance = 0
        self.max_patrol_distance = 250

        self.player = self.game_manager.player
        self.collision_mask = ['ladder', 'enemy_projectile', 'enemy', 'player', 'player_projectile', 'portal']

        # create tracking and attack distance
        self.is_ranged = is_ranged
        if self.is_ranged:
            self.tracking_range = 500
            self.attack_range = 400
        else:
            self.tracking_range = 400
            self.attack_range = 30

        self.speed = speed
        self.weight = 1.2

        self.damage = damage
        self.health = health

        self.cooldown = cooldown
        self.cooldown_count = 0
        self.points = points
        self.projectile = None

        # Mana attributes for enemy
        self.mana_max = mana_max
        self.mana = self.mana_max
        self.mana_recharge_rate = mana_recharge_rate
        self.mana_time = 0

    def update(self):
        self.recharge_mana()
        # Update state before updating frame
        self.state_update()
        self.frame_update()
        self.movement()
        # Add all movements
        self.position.add(self.velocity)
        self.velocity.multiply(0.80)

    def movement(self):
        speed = self.speed
        # Gravity movement
        if self.state.GRAVITY:
            self.velocity.y += self.weight

        # Patrol movements
        if self.state.PATROL:
            self.state.ATTACK1 = False
            self.speed *= 0.5
            if self.patrol_right:
                self.state.RIGHT = True
                self.state.LEFT = False
            else:
                self.state.RIGHT = False
                self.state.LEFT = True

            self.patrolled_distance += abs(self.velocity.x)

            if self.patrolled_distance >= self.max_patrol_distance:
                self.patrol_right = not self.patrol_right
                self.patrolled_distance = 0

        # Move left/right
        if self.state.RIGHT:
            self.velocity += Vector(1, 0) * self.speed
            self.idle_frame = [0, 0]
        elif self.state.LEFT:
            self.velocity += Vector(-1, 0) * self.speed
            self.idle_frame = [2, 0]
        self.speed = speed

    def state_update(self):
        # Update ATTACK1_COOLDOWN state
        if self.state.ATTACK1_COOLDOWN:
            self.cooldown_count += 1
            if self.cooldown_count == self.cooldown:
                self.state.ATTACK1_COOLDOWN = False
                self.cooldown_count = 0

        # shortest distance
        distance_to_player = math.sqrt((self.player.position.x - self.position.x) ** 2 +
                                       (self.player.position.y - self.position.y) ** 2)

        # If enemy close to player, attack player
        if distance_to_player <= self.attack_range:
            self.state.ATTACK1 = True
            self.state.PATROL = False
            self.idle_frame = [0, 0]
            if self.player.position.x < self.position.x:
                self.idle_frame = [2, 0]

        # If enemy is far from player, move towards player position
        elif self.player.position.x - 25 > self.position.x and distance_to_player <= self.tracking_range:
            self.state.RIGHT = True
            self.state.LEFT = False
            self.state.PATROL = False
        elif self.player.position.x + 25 < self.position.x and distance_to_player <= self.tracking_range:
            self.state.LEFT = True
            self.state.RIGHT = False
            self.state.PATROL = False

        # Enemy patrol state
        else:
            self.state.PATROL = True

    def frame_update(self):
        if self.state.FLINCH:
            self.flinch_animation()

        elif self.state.ATTACK1:
            if not self.state.ATTACK1_COOLDOWN:
                self.attack1_animation()

        elif self.state.RIGHT and not self.state.LEFT:
            self.move_right_animation()

        elif self.state.LEFT and not self.state.RIGHT:
            self.move_left_animation()
        self.frame_count += 1

    def flinch_animation(self):
        # Lock-in FLINCH state
        self.state.LEFT, self.state.RIGHT, self.state.JUMP = False, False, False
        self.state.PUNCH, self.state.SHOOT = False, False
        self.state.PUNCH_END = True

        # Choosing correct frame
        self.frame_index = [3, 0]
        if self.idle_frame[0] == 0:
            self.frame_index = [1, 0]

        # Control duration of state
        if self.frame_count > 0:
            self.frame_count = -5
        if self.frame_count % 6 == 0:
            self.state.FLINCH = False

    def attack1_animation(self):
        # Stops left/right movement during attack
        self.state.RIGHT, self.state.LEFT = False, False

        # Choosing correct row
        if self.idle_frame[0] == 0:
            self.frame_index[1] = 5
        elif self.frame_index[1] != 6:
            self.frame_index = [0, 6]

        # Ensuring the column number is not greater than number of frames in the row
        if self.frame_index[0] >= self.attack_frames:
            self.frame_index[0] = 0

        # Reset count so animation is always played the same
        if self.frame_count > 0:
            if self.name == 'warrior':
                self.frame_count = -5
                self.fps = 6
            else:
                self.frame_count = -15
                self.fps = 16

        # Control FPS
        if self.frame_count % self.fps == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % self.attack_frames

            # Damage condition for warrior
            if self.name == 'warrior' and self.frame_index[0] == 1:
                dmg = 1
                if self.game_manager.interaction_manager.is_overlapping(self, self.player):
                    self.player.deal_damage(dmg)

            # Damage condition for shaman
            elif self.name == 'shaman' and self.frame_index[0] == 3:
                self.shoot()

            # Damage condition for hunter
            elif self.name == 'hunter' and self.frame_index[0] == 3:
                self.shoot()

            # Turns off animation at last frame
            if self.frame_index[0] == 0:
                self.state.ATTACK1 = False
                self.state.ATTACK1_COOLDOWN = True

    def move_right_animation(self):
        # Choosing correct row
        self.frame_index[1] = 1
        if self.frame_index[0] >= self.walk_frames:
            self.frame_index[0] = 0

        # Control FPS
        if self.frame_count % 10 == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % self.walk_frames

    def move_left_animation(self):
        # Choosing correct row
        self.frame_index[1] = 2
        if self.frame_index[0] >= self.walk_frames:
            self.frame_index[0] = 0

        # Control FPS
        if self.frame_count % 10 == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % self.walk_frames

    def shoot(self):
        if self.mana >= 40:
            self.mana -= 40

            move_right = True
            adjust_x = 10
            if self.frame_index[1] == 6:
                move_right = False
                adjust_x = -10

            self.projectile = Projectile(kind='enemy_projectile', game_manager=self.game_manager,
                                         position=Vector(self.position.x + adjust_x, self.position.y), speed=1.2)
            self.projectile.is_right = move_right
            self.projectile.is_red = False
            self.game_manager.add_entity(self.projectile)

    def deal_damage(self, amount):
        self.state.FLINCH = True
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        self.game_manager.score_counter.add_score(self.points)
        self.destroy()

    def recharge_mana(self):
        if self.mana_time % self.mana_recharge_rate == 0:
            self.mana = min(self.mana + self.mana_recharge_rate, self.mana_max)
        self.mana_time += 1
