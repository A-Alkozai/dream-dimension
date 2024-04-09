import random

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from state import State
from entity import Entity
from effects import Effect
from projectile import Projectile


class Player(Entity):
    def __init__(self, lives, **kwargs):
        super().__init__(**kwargs)

        # Setting initial state
        self.state = State()
        self.state.IDLE = True
        self.state.PUNCH_END = True
        self.idle_frame = [0, 0]

        # Number of frames per animation type
        self.walk_frames = 8
        self.jump_frames = 2
        self.attack_frames = 4
        self.flinch_frames = 2

        # Mask collisions for certain entities
        self.collision_mask = ['ladder', 'player_projectile', 'enemy', 'enemy_projectile', 'portal', 'drop', 'sfx']

        self.lives = lives
        self.weight = 1.5
        self.speed = 1

        # Projectile attributes
        self.projectile = None
        self.shotRed = False
        self.shotPurple = False
        self.shotSpecial = False
        self.shotSpecial2 = False

        # Mana attributes
        self.mana = 120
        self.mana_max = 120
        self.mana_recharge_rate = 0.125
        self.mana_time = 0

    def update(self):
        self.recharge_mana()
        # Update state
        self.state_update()
        # Check for interactions with map objects
        self.interactions()
        # Update frame
        self.frame_update()
        # Calculate movements then add them
        self.movement()
        self.position.add(self.velocity)
        self.velocity.multiply(0.80)


    def movement(self):
        # Climbing ladder
        if self.state.CLIMB:
            self.climb_movement()
        elif self.state.JUMP and self.state.IN_JUMP:
            self.velocity += Vector(0, -6) * self.speed

        if self.state.GRAVITY:
            self.velocity.y += self.weight

        # Move left/right
        if self.state.RIGHT:
            self.velocity += Vector(1, 0) * self.speed
            self.idle_frame = [0, 0]
        if self.state.LEFT:
            self.velocity += Vector(-1, 0) * self.speed
            self.idle_frame = [2, 0]

    def state_update(self):
        # List containing every block on current map
        all_entities = self.game_manager.all_entities
        ground_blocks = [entity for entity in all_entities if entity.kind == 'block']

        # Update GROUNDED state
        for block in ground_blocks:
            is_touching = self.game_manager.interaction_manager.is_colliding(self, block)[0]
            block_side = self.game_manager.interaction_manager.is_colliding(self, block)[1]
            # Only if player is on top of a block
            if is_touching and block_side == 'top':
                self.state.GROUNDED = True
                self.state.FALL = False
                break
            self.state.GROUNDED = False
            self.state.FALL = True

    # Update frame based on state
    def frame_update(self):
        if self.state.FLINCH:
            self.flinch_animation()

        elif self.state.PUNCH and self.state.JUMP:
            self.jump_punch_animation()

        elif self.state.PUNCH and self.state.FALL:
            self.fall_punch_animation()

        elif self.state.SHOOT and self.state.PUNCH_END:
            self.shooting_animation()

        elif self.state.PUNCH:
            self.punching_animation()

        elif self.state.JUMP:
            self.jumping_animation()

        elif self.state.FALL:
            self.falling_animation()

        elif self.state.RIGHT and not self.state.LEFT:
            self.move_right_animation()

        elif self.state.LEFT and not self.state.RIGHT:
            self.move_left_animation()

        else:
            self.idle_animation()
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

    def jump_punch_animation(self):
        # self.state.RIGHT, self.state.LEFT = False, False
        self.state.PUNCH_END, self.state.SHOOT = False, False

        # Choosing correct row
        self.frame_index[1] = 8
        if self.idle_frame == [0, 0]:
            self.frame_index[1] = 7

        # Ensuring the column number is not greater than number of frames in the row
        if self.frame_index[0] >= self.attack_frames:
            self.frame_index[0] = 0

        # Reset count so animation is always played the same
        if self.frame_count > 0:
            self.frame_count = -7

        # Ensures player falls during midair attack
        if self.frame_count % 8 == 0:
            self.state.JUMP = False
            self.state.FALL = True

        # Control FPS of animation
        if self.frame_count % 4 == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % self.attack_frames

            # Damage at 2nd frame
            if self.frame_index[0] == 1:
                for entity in self.game_manager.all_entities:
                    dmg = 2
                    target = 'enemy'
                    # If overlapping with target
                    if ((entity.name == target and entity != self) and
                            self.game_manager.interaction_manager.is_overlapping(self, entity)):

                        # Create impact sfx
                        self.effect = Effect(name='impact', game_manager=self.game_manager,
                                             position=self.position + Vector(5, -15))
                        if self.frame_index[1] == 5:
                            self.effect.rotation = 3.14
                            self.effect.position += Vector(-10, 30)
                        self.game_manager.add_entity(self.effect)
                        self.effect = None

                        # Deal damage to a single target
                        entity.deal_damage(dmg)
                        break

            if self.frame_index[0] == 0:
                self.state.PUNCH = False
                self.state.PUNCH_END = True

    def fall_punch_animation(self):
        # self.state.RIGHT, self.state.LEFT = False, False
        self.state.PUNCH_END, self.state.SHOOT = False, False

        # Choosing correct row
        self.frame_index[1] = 8
        if self.idle_frame == [0, 0]:
            self.frame_index[1] = 7

        # Ensuring the column number is not greater than number of frames in the row
        if self.frame_index[0] >= self.attack_frames:
            self.frame_index[0] = 0

        # Reset count so animation is always played the same
        if self.frame_count > 0:
            self.frame_count = -7

        # Control FPS of animation
        if self.frame_count % 4 == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % self.attack_frames

            # Damage at 2nd frame
            if self.frame_index[0] == 1:
                for entity in self.game_manager.all_entities:
                    dmg = 2
                    target = 'enemy'
                    if ((entity.name == target and entity != self) and
                            self.game_manager.interaction_manager.is_overlapping(self, entity)):
                        self.effect = Effect(name='impact', game_manager=self.game_manager,
                                             position=self.position + Vector(5, -15))
                        if self.frame_index[1] == 5:
                            self.effect.rotation = 3.14
                            self.effect.position += Vector(-10, 30)
                        self.game_manager.add_entity(self.effect)
                        entity.deal_damage(dmg)
                        break

            if self.frame_index[0] == 0:
                self.state.PUNCH = False
                self.state.PUNCH_END = True

    def shooting_animation(self):
        self.state.RIGHT, self.state.LEFT, self.state.JUMP = False, False, False,
        self.state.PUNCH = False

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
            self.frame_index[0] = (self.frame_index[0] + 1) % self.attack_frames

            # Create projectile at 4th frame
            if self.frame_index[0] == 3:
                self.shoot()

            # Turns off animation at last frame
            if self.frame_index[0] == 0:
                self.state.SHOOT = False

    def punching_animation(self):
        # Stops left/right movement during attack
        self.state.RIGHT, self.state.LEFT = False, False
        self.state.PUNCH_END, self.state.SHOOT = False, False

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
            self.frame_count = -4

        # Control FPS
        if self.frame_count % 5 == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % self.attack_frames

            # Damage at 2nd frame
            if self.frame_index[0] == 1:
                for entity in self.game_manager.all_entities:
                    dmg = 1
                    target = 'enemy'
                    if ((entity.kind == target and entity != self) and
                            self.game_manager.interaction_manager.is_overlapping(self, entity)):
                        self.effect = Effect(name='impact', game_manager=self.game_manager,
                                             position=self.position + Vector(5, -15))
                        if self.frame_index[1] == 5:
                            self.effect.rotation = 3.14
                            self.effect.position += Vector(-10, 30)
                        self.game_manager.add_entity(self.effect)
                        entity.deal_damage(dmg)
                        break

            # Turns off animation at last frame
            if self.frame_index[0] == 0:
                self.state.PUNCH = False
                self.state.PUNCH_END = True

    def jumping_animation(self):
        self.state.IN_JUMP = True
        self.state.GROUNDED = False

        # Choosing correct row
        self.frame_index = [0, 4]
        if self.idle_frame == [0, 0]:
            self.frame_index = [0, 3]

        # Reset count so animation is always played the same
        if self.frame_count > 0:
            self.frame_count = -7

        # Control FPS and turns off animation
        if self.frame_count % 8 == 0:
            self.state.JUMP = False
            self.state.IN_JUMP = False
            self.state.FALL = True

    def falling_animation(self):
        # Choosing correct row
        self.frame_index = [1, 4]
        if self.idle_frame == [0, 0]:
            self.frame_index = [1, 3]

        # Fall animation until touches ground
        if self.state.GROUNDED:
            self.state.FALL = False

    def move_right_animation(self):
        # Choosing correct row
        self.frame_index[1] = 1
        if self.frame_index[0] >= self.walk_frames:
            self.frame_index[0] = 0

        # Control FPS
        if self.frame_count % 5 == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % self.walk_frames

    def move_left_animation(self):
        # Choosing correct row
        self.frame_index[1] = 2
        if self.frame_index[0] >= self.walk_frames:
            self.frame_index[0] = 0

        # Control FPS
        if self.frame_count % 5 == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % self.walk_frames

    def idle_animation(self):
        self.frame_index[0] = self.idle_frame[0]
        self.frame_index[1] = self.idle_frame[1]

    def climb_movement(self):
        ladders = [entity for entity in self.game_manager.all_entities if entity.kind == 'ladder']

        # update on_ladder
        for ladder in ladders:
            if self.game_manager.interaction_manager.is_overlapping(self, ladder):
                self.state.ON_LADDER = True
                break
            else:
                self.state.ON_LADDER = False
        # ladder climbing movement
        if self.state.ON_LADDER:
            self.velocity.y += -3

    def interactions(self):
        drops = [entity for entity in self.game_manager.all_entities if entity.kind == 'drop']

        for drop in drops:
            if self.game_manager.interaction_manager.is_overlapping(self, drop):
                if drop.name == 'heart':
                    self.lives += 1
                    self.game_manager.remove_entity(drop)
                elif drop.name == 'bonus':
                    self.game_manager.score_counter.add_score(random.randint(3, 30))
                    self.game_manager.remove_entity(drop)
                elif drop.name == 'learn_red':
                    self.shotRed = True
                    self.game_manager.remove_entity(drop)
                elif drop.name == 'learn_purple':
                    self.shotPurple = True
                    self.game_manager.remove_entity(drop)
                elif drop.name == 'learn_sp1':
                    self.shotSpecial = True
                    self.game_manager.remove_entity(drop)
                elif drop.name == 'learn_sp2':
                    self.shotSpecial2 = True
                    self.game_manager.remove_entity(drop)
                elif drop.name == 't1':
                    text = Entity(kind='text', position=Vector(self.game_manager.CANVAS_WIDTH/2, 400),
                                  img_url="images/texts/text1.png", img_dest_dim=(1287*0.8, 112*0.8))
                    self.game_manager.add_text(text)
                elif drop.name == 't2':
                    text = Entity(kind='text', position=Vector(self.game_manager.CANVAS_WIDTH/2, 400),
                                  img_url="images/texts/text2.png", img_dest_dim=(1113*0.8, 112*0.8))
                    self.game_manager.add_text(text)
                elif drop.name == 't3':
                    text = Entity(kind='text', position=Vector(self.game_manager.CANVAS_WIDTH/2, 400),
                                  img_url="images/texts/text3.png", img_dest_dim=(661*0.8, 109*0.8))
                    self.game_manager.add_text(text)
                elif drop.name == 't4':
                    text = Entity(kind='text', position=Vector(self.game_manager.CANVAS_WIDTH/2, 400),
                                  img_url="images/texts/controls.png", img_dest_dim=(1169*0.8, 519*0.8))
                    self.game_manager.add_text(text)
                elif drop.name == 't5':
                    text = Entity(kind='text', position=Vector(self.game_manager.CANVAS_WIDTH/2, 400),
                                  img_url="images/texts/text5.png", img_dest_dim=(1278*0.8, 162*0.8))
                    self.game_manager.add_text(text)
                elif drop.name == 't6':
                    text = Entity(kind='text', position=Vector(self.game_manager.CANVAS_WIDTH/2, 400),
                                  img_url="images/texts/text6.png", img_dest_dim=(707*0.8, 112*0.8))
                    self.game_manager.add_text(text)
                elif drop.name == 't7':
                    text = Entity(kind='text', position=Vector(self.game_manager.CANVAS_WIDTH/2, 400),
                                  img_url="images/texts/text7.png", img_dest_dim=(1286*0.8, 212*0.8))
                    self.game_manager.add_text(text)
                elif drop.name == 't8':
                    text = Entity(kind='text', position=Vector(self.game_manager.CANVAS_WIDTH/2, 400),
                                  img_url="images/texts/text8.png", img_dest_dim=(791*0.8, 286*0.8))
                    self.game_manager.add_text(text)
                elif drop.name == 't9':
                    text = Entity(kind='text', position=Vector(self.game_manager.CANVAS_WIDTH/2, 400),
                                  img_url="images/texts/text9.png", img_dest_dim=(1151*0.8, 280*0.8))
                    self.game_manager.add_text(text)
                elif drop.name == 't10':
                    text = Entity(kind='text', position=Vector(self.game_manager.CANVAS_WIDTH/2, 400),
                                  img_url="images/texts/text10.png", img_dest_dim=(642*0.8, 269*0.8))
                    self.game_manager.add_text(text)
                elif drop.name == 't11':
                    text = Entity(kind='text', position=Vector(self.game_manager.CANVAS_WIDTH/2, 400),
                                  img_url="images/texts/text11.png", img_dest_dim=(703*0.8, 274*0.8))
                    self.game_manager.add_text(text)
                elif drop.name == 't12':
                    text = Entity(kind='text', position=Vector(self.game_manager.CANVAS_WIDTH/2, 400),
                                  img_url="images/texts/text12.png", img_dest_dim=(1291*0.8, 162*0.8))
                    self.game_manager.add_text(text)

    def shoot(self):
        # Initialise direction of projectile
        move_right = True
        adjust_x = 10
        if self.frame_index[1] == 10:
            move_right = False
            adjust_x = -10

        # Spawn projectile
        if self.state.SLOT1:
            if self.shotRed and self.mana >= 40:
                self.mana -= 40
                self.projectile = Projectile(kind='player_projectile', name='1', game_manager=self.game_manager,
                                             damage=0.5, position=Vector(self.position.x + adjust_x, self.position.y),
                                             speed=1.2)
        elif self.state.SLOT2:
            if self.shotPurple and self.mana >= 80:
                self.mana -= 80
                self.projectile = Projectile(kind='player_projectile', name='2', game_manager=self.game_manager,
                                             damage=0, position=Vector(self.position.x + adjust_x, self.position.y),
                                             speed=1.6)
        elif self.state.SLOT3:
            if self.shotSpecial and self.mana >= 80:
                self.mana -= 80
                self.projectile = Projectile(kind='player_projectile', name='3', game_manager=self.game_manager,
                                             damage=1.5, position=Vector(self.position.x + adjust_x, self.position.y),
                                             speed=1.3)
        elif self.state.SLOT4:
            if self.shotSpecial2 and self.mana == 120:
                self.mana -= 120
                choice = random.randint(1, 2)
                dmg = 0
                if choice == 1:
                    dmg = 10
                self.projectile = Projectile(kind='player_projectile', name='4', game_manager=self.game_manager,
                                             damage=dmg, position=Vector(self.position.x + adjust_x, self.position.y),
                                             speed=1.4)

        if self.projectile is not None:
            self.projectile.is_right = move_right
            self.game_manager.add_entity(self.projectile)
        self.projectile = None

    def deal_damage(self, amount):
        self.state.FLINCH = True
        self.lives -= amount
        if self.lives <= 0:
            self.die()

    def deal_knockback(self, amount, right):
        if right:
            self.velocity.add(Vector(amount, 0))
        else:
            self.velocity.add(Vector(-amount, 0))

    def die(self):
        # Remove player from entity list
        self.destroy()
        # Update score tracker
        score = self.game_manager.score_counter.score
        self.game_manager.welcome_screen.highscore_screen.scores.append(score)
        # Reset the max level reached
        self.game_manager.score_counter.max_level = 0
        # Reset learnt attacks
        self.shotRed, self.shotPurple, self.shotSpecial, self.shotSpecial2 = False, False, False, False
        # Change to welcome screen
        self.game_manager.clear_screen()
        self.game_manager.welcome_screen.show_welcome_screen = True

    def key_down(self, key):
        if key == simplegui.KEY_MAP["1"]:
            self.state.SLOT1 = True
            self.state.SLOT2 = False
            self.state.SLOT3 = False
            self.state.SLOT4 = False
        if key == simplegui.KEY_MAP["2"]:
            self.state.SLOT1 = False
            self.state.SLOT2 = True
            self.state.SLOT3 = False
            self.state.SLOT4 = False
        if key == simplegui.KEY_MAP["3"]:
            self.state.SLOT1 = False
            self.state.SLOT2 = False
            self.state.SLOT3 = True
            self.state.SLOT4 = False
        if key == simplegui.KEY_MAP["4"]:
            self.state.SLOT1 = False
            self.state.SLOT2 = False
            self.state.SLOT3 = False
            self.state.SLOT4 = True
        if key == simplegui.KEY_MAP["space"] and self.state.GROUNDED:
            self.state.JUMP = True
        if key == simplegui.KEY_MAP['w']:
            self.state.CLIMB = True
        if key == simplegui.KEY_MAP["a"]:
            self.state.LEFT = True
        if key == simplegui.KEY_MAP["d"]:
            self.state.RIGHT = True
        if key == simplegui.KEY_MAP["f"]:
            self.state.PUNCH = True
        if key == simplegui.KEY_MAP["q"]:
            self.state.SHOOT = True
        if key == simplegui.KEY_MAP['e']:
            self.state.INTERACT = True

    def key_up(self, key):
        if key == simplegui.KEY_MAP["a"]:
            self.state.LEFT = False
        if key == simplegui.KEY_MAP["d"]:
            self.state.RIGHT = False
        if key == simplegui.KEY_MAP['w']:
            self.state.CLIMB = False
            self.state.ON_LADDER = False
        if key == simplegui.KEY_MAP['e']:
            self.state.INTERACT = False

    def recharge_mana(self):
        if self.mana_time % self.mana_recharge_rate == 0:
            self.mana = min(self.mana + self.mana_recharge_rate, self.mana_max)
        self.mana_time += 1
