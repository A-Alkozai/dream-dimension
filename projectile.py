import random
from effects import Effect
from vector import Vector
from state import State
from entity import Entity


class Projectile(Entity):
    def __init__(self, speed=1.2, damage=1, **kwargs):
        self.img_url = 'images/sprites/projectiles/projectiles.png'
        self.img_dest_dim = (60, 60)
        super().__init__(img_url=self.img_url, column=30, row=6, img_dest_dim=self.img_dest_dim, **kwargs)

        # Determine animation attributes based on projectile name
        match self.name:
            case '1':  # Red
                self.frame_index = [0, 4]
                self.totalFrames = 15
                self.fps = 3
            case '2':  # Purple
                self.frame_index = [0, 1]
                self.totalFrames = 10
                self.img_dest_dim = (40, 50)
                self.fps = 3
            case '3':  # Sp1
                self.frame_index = [0, 3]
                self.totalFrames = 30
                self.fps = 1
            case '4':  # Sp2
                self.frame_index = [0, 0]
                self.totalFrames = 30
                self.fps = 1
            case '5':  # Blue
                self.frame_index = [0, 5]
                self.totalFrames = 15
                self.fps = 3
            case '6':  # Arrow
                self.frame_index = [0, 2]
                self.totalFrames = 30
                self.img_dest_dim = (100, 100)
                self.fps = 3

        # Initialising states
        self.state = State()
        self.state.GRAVITY = False

        # Creation of collision mask
        self.collision_mask = ['ladder', 'player_projectile', 'player', 'enemy',
                               'enemy_projectile', 'portal', 'drop', 'sfx']

        # Determine attributes of projectile
        self.is_right = True
        self.move = True
        self.tick = False
        self.time = 0
        self.speed = speed
        self.damage = damage

        # Determine targets of projectile, based upon user
        if self.kind.startswith('player'):
            self.target_kinds = ['enemy', 'block', 'enemy_projectile']
        elif self.kind.startswith('enemy'):
            self.target_kinds = ['player', 'block', 'player_projectile']

    def update(self):
        # Set direction of projectile
        self.set_direction(self.is_right)
        # Update frame
        self.frame_update()
        # Calculate and add movement
        self.movement()
        self.velocity.y = 0
        self.position.add(self.velocity)
        self.velocity.multiply(0.85)
        # Option for timed explosion
        self.timer()
        # Ensure projectile is destroyed outside of canvas
        self.boundaries()
        # Check for collisions
        self.collision()

    def movement(self):
        if self.move:
            # Left/Right movement
            if self.state.RIGHT:
                self.velocity += Vector(1, 0) * self.speed
            if self.state.LEFT:
                self.velocity += Vector(-1, 0) * self.speed

    def frame_update(self):
        if self.frame_count % self.fps == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % self.totalFrames
        self.frame_count += 1

    def set_direction(self, is_right):
        # Determine the projectile direction
        # Determine rotation of projectile based on direction
        self.state.RIGHT = False
        self.state.LEFT = True
        self.rotation = 3
        if is_right:
            self.state.RIGHT = True
            self.state.LEFT = False
            self.rotation = 0

    def boundaries(self):
        # Destroys projectile if collision with canvas boundary occurs
        if self.position.x <= 0 or self.position.x >= 1920 or self.position.y <= 0 or self.position.y >= 1080:
            self.destroy()

    # Calculate if projectile has collided with a target
    def collision(self):
        targets = [entity for entity in self.game_manager.all_entities if entity.kind in self.target_kinds]
        for target in targets:
            if self.game_manager.interaction_manager.is_colliding(self, target)[0]:
                # Collision with block
                if target.kind == 'block':
                    if self.name == '2':
                        self.tick = True
                    else:
                        self.destroy()
                # Collision with projectile
                elif target.kind == 'enemy_projectile' or target.kind == 'player_projectile':
                    self.projectile_collision(target)
                # Collision with enemy
                else:
                    self.enemy_collision(target)
                    break

    # Destroy itself or the other projectile
    def projectile_collision(self, target):
        number = random.randint(1, 2)
        if number == 1:
            self.destroy()
        else:
            target.destroy()

    # Damage enemy
    def enemy_collision(self, target):
        # do damage and knock-back to target
        if self.name != '2':
            if target not in self.collision_mask:
                target.deal_knockback(10, self.is_right)
                self.collision_mask.append(target)
            target.deal_damage(self.damage)
            self.destroy()
        else:
            self.position = target.position
            self.velocity = Vector(0, 0)
            self.move = False
            self.tick = True

    def timer(self):
        if self.tick:
            self.time += 1
            if self.time == 40:
                self.destroy()

    def destroy(self):
        super().destroy()
        if self.name == '2':
            position = Vector(self.position.x, self.position.y-50)
            self.effect = Effect(name='player_explosion', position=position, game_manager=self.game_manager)
        elif self.name == '5':
            self.effect = Effect(name='water_spiral', game_manager=self.game_manager, position=self.position)
        elif self.name == '6':
            self.effect = Effect(name='fire_spiral', game_manager=self.game_manager, position=self.position)
        if self.effect is not None:
            self.game_manager.add_entity(self.effect)
            self.effect = None
