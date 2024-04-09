import random

from projectile import Projectile
from vector import Vector
from state import State
from entity import Entity
from effects import Effect
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

        # Initialising the states
        self.state = State()
        self.state.PATROL = True
        self.idle_frame = [0, 0]

        # Patrol conditions
        self.patrol_right = True
        self.patrolled_distance = 0
        self.max_patrol_distance = 250

        # Initialising the player and collision masks
        self.player = self.game_manager.player
        self.collision_mask = ['ladder', 'enemy_projectile', 'enemy', 'player', 'player_projectile', 'portal', 'drop', 'sfx']

        # Create tracking and attack distance
        self.is_ranged = is_ranged
        if self.is_ranged:
            self.tracking_range = 500
            self.attack_range = 400
        elif self.name == 'bomber':
            self.tracking_range = 400
            self.attack_range = 100
        else:
            self.tracking_range = 400
            self.attack_range = 30

        # Movement speed
        self.speed = speed
        self.weight = 1.5

        # Health/Dmg
        self.damage = damage
        self.health = health

        # Animation speed
        self.fps = 1

        # Cooldown for attack
        self.cooldown = cooldown
        self.cooldown_count = 0

        # Points given upon death
        self.points = points

        # Mana attributes
        self.mana_max = mana_max
        self.mana = self.mana_max
        self.mana_recharge_rate = mana_recharge_rate
        self.mana_time = 0

        # Projectile attributes
        self.projectile = None

    def update(self):
        self.recharge_mana()
        # Update state
        self.state_update()
        # Update frame
        self.frame_update()
        # Calculate then add movements
        self.movement()
        self.position.add(self.velocity)
        self.velocity.multiply(0.80)

    def movement(self):
        speed = self.speed
        # Gravity movement
        if self.state.GRAVITY:
            self.velocity.y += self.weight

        # Patrol movements at 1/2 normal speed
        if self.state.PATROL:
            self.state.ATTACK1 = False
            self.speed *= 0.5
            if self.patrol_right:
                self.state.RIGHT = True
                self.state.LEFT = False
            else:
                self.state.RIGHT = False
                self.state.LEFT = True

            # Change of direction after certain distance has been walked
            self.patrolled_distance += abs(self.velocity.x)
            if self.patrolled_distance >= self.max_patrol_distance:
                self.patrol_right = not self.patrol_right
                self.patrolled_distance = 0

        # Left/Right movement
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

        # Shortest distance to player
        distance_to_player = math.sqrt((self.player.position.x - self.position.x) ** 2 +
                                       (self.player.position.y - self.position.y) ** 2)

        # If enemy close to player, attack player
        if distance_to_player <= self.attack_range:
            self.state.ATTACK1 = True
            self.state.PATROL = False
            self.idle_frame = [0, 0]
            if self.player.position.x < self.position.x:
                self.idle_frame = [2, 0]

        # If enemy is far from player, but within sight, move towards player position
        elif self.player.position.x - 25 > self.position.x and distance_to_player <= self.tracking_range:
            self.state.RIGHT = True
            self.state.LEFT = False
            self.state.PATROL = False
        elif self.player.position.x + 25 < self.position.x and distance_to_player <= self.tracking_range:
            self.state.LEFT = True
            self.state.RIGHT = False
            self.state.PATROL = False

        # If outside of sight range, patrol state activated
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
            elif self.name == 'fighter':
                self.frame_count = -5
                self.fps = 6
            elif self.name == 'swordsman':
                self.frame_count = -4
                self.fps = 5
            else:
                self.frame_count = -15
                self.fps = 16

        # Control FPS
        if self.frame_count % self.fps == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % self.attack_frames

            # Orcs
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

            # Skeletons
            # Damage condition for fighter
            elif self.name == 'fighter' and self.frame_index[0] == 2:
                dmg = 1
                if self.game_manager.interaction_manager.is_overlapping(self, self.player):
                    self.player.deal_damage(dmg)
            elif self.name == 'swordsman' and self.frame_index[0] == 3:
                dmg = 1
                if self.game_manager.interaction_manager.is_overlapping(self, self.player):
                    self.player.deal_damage(dmg)
            elif self.name == 'bomber':
                self.die()

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

            if self.name == 'shaman':
                self.projectile = Projectile(kind='enemy_projectile', name='5', game_manager=self.game_manager,
                                             position=Vector(self.position.x + adjust_x, self.position.y), speed=1.2)
            elif self.name == 'hunter':
                self.projectile = Projectile(kind='enemy_projectile', name='6', game_manager=self.game_manager,
                                             position=Vector(self.position.x + adjust_x, self.position.y), speed=1.2)

            self.projectile.is_right = move_right
            self.game_manager.add_entity(self.projectile)

    def deal_damage(self, amount):
        self.state.FLINCH = True
        self.health -= amount
        if self.health <= 0:
            self.die()

    def deal_knockback(self, amount, right):
        if right:
            self.velocity.add(Vector(amount, 0))
        else:
            self.velocity.add(Vector(-amount, 0))

    def item_drops(self):
        chance = random.randint(1, 15)
        if chance == 15:
            heart_drop = Entity(kind='drop', name='heart', position=self.position, img_url='images/heart.png',
                                img_dest_dim=(40, 40))
            self.game_manager.add_entity(heart_drop)
        chance = random.randint(1, 20)
        if chance == 20:
            bonus_drop = Entity(kind='drop', name='bonus', position=self.position, img_dest_dim=(50, 50),
                                img_url='images/interactables/dice.png')
            self.game_manager.add_entity(bonus_drop)

    def die(self):
        self.game_manager.score_counter.add_score(self.points)
        self.destroy()
        if self.name == 'bomber':
            position = Vector(self.position.x, self.position.y-100)
            self.effect = Effect('enemy_explosion', position, self.game_manager)
        else:
            self.effect = Effect('blood', self.position, self.game_manager)
        self.game_manager.add_entity(self.effect)
        self.item_drops()

    def recharge_mana(self):
        if self.mana_time % self.mana_recharge_rate == 0:
            self.mana = min(self.mana + self.mana_recharge_rate, self.mana_max)
        self.mana_time += 1
