class State:

    # Global states
    GRAVITY = True
    RIGHT = False
    LEFT = False
    FLINCH = False
    DEAD = False

    # Player states
    IDLE = False

    GROUNDED = False
    JUMP = False
    IN_JUMP = False
    FALL = False

    ON_LADDER = False
    CLIMB = False

    PUNCH = False
    PUNCH_END = False
    SHOOT = False

    # Enemy states
    ATTACK1 = False
    ATTACK1_COOLDOWN = False
    ATTACK2 = False
    PATROL = False









# class State(Entity):
#     def __init__(self, name, walk_frames=0, jump_frames=0, attack_frames=0, dmg_frames=0, health_max=1, mana_max=120,
#                  mana_recharge_rate=5, gravity_strength=1.5, player=None, projectile=None, interaction=None, speed=1,
#                  **kwargs):
#
#         # different states
#         self.GRAVITY = True
#         self.IDLE = True
#         self.PATROL = False
#         self.JUMP = False
#         self.FALL = False
#         self.LEFT = False
#         self.RIGHT = False
#         self.ATTACK1 = False
#         self.ATTACK1_END = True
#         self.ATTACK1_COOLDOWN = False
#         self.ATTACK2 = False
#         self.SHOOTING = False
#         self.HURT = False
#         self.HIT = False
#         self.DEAD = False
#
#         # ladders
#         self.CLIMB = False
#
#         # patrol conditions
#         self.patrol_right = True
#         self.patrolled_distance = 0
#         self.max_patrol_distance = 250
#
#         # default idle frame
#         self.idle_frame = [0, 0]
#         self.fps = 3
#         self.in_jump = False
#         self.is_ranged = False
#
#         # player & projectile object
#         self.player = player
#         self.interaction = interaction
#
#         self.projectile = projectile
#         self.count = 0
#         self.score = 0
#
#         # general & gravity speed
#         self.speed = speed
#         self.weight = gravity_strength
#
#         # health attributes
#         self.health = health_max
#         self.health_max = health_max
#         self.damaged = 0
#
#         # mana attributes
#         self.mana = mana_max
#         self.mana_max = mana_max
#         self.mana_recharge_rate = mana_recharge_rate
#         self.mana_recharge_timer = simplegui.create_timer(1000, self.recharge_mana)
#
#         super().__init__(name, **kwargs)
#
#     def state_update(self):
#         pass
#
#     def deal_damage(self, amount):
#         self.HURT = True
#
#         self.health -= amount
#
#         if self.health <= 0:
#             self.die()
#
#     def die(self):
#         if self.name == 'enemy':
#             self.game_manager.scorecounter.add_score(self.score)
#         self.destroy()
#
#     def update(self):
#         # Update state before updating frame
#         self.state_update()
#         self.frame_update()
#         self.movement()
#         # Add all movements
#         self.position.add(self.velocity)
#         self.velocity.multiply(0.80)
#










#     def movement(self):
#         speed = self.speed
#
#         if self.CLIMB:
#             ladders = [entity for entity in self.game_manager.all_entities if entity.name == 'ladder']
#
#             # update on_ladder
#             for ladder in ladders:
#                 if self.game_manager.interaction_manager.is_overlapping(self, ladder):
#                     self.on_ladder = True
#                     break
#                 else:
#                     self.on_ladder = False
#             # ladder climbing movement
#             if self.on_ladder:
#                 self.velocity.y += (Vector(0, -3) * self.speed).y
#
#         elif self.JUMP and self.in_jump:
#             self.velocity += Vector(0, -6) * self.speed
#         if self.GRAVITY:
#             self.velocity.y += self.weight
#
#         # Patrol movements
#         if self.PATROL:
#             self.ATTACK1 = False
#             self.ATTACK1_END = True
#             self.speed *= 0.5
#             if self.patrol_right:
#                 self.RIGHT = True
#                 self.LEFT = False
#             else:
#                 self.RIGHT = False
#                 self.LEFT = True
#             self.patrolled_distance += abs(self.velocity.x)
#             if self.patrolled_distance >= self.max_patrol_distance:
#                 self.patrol_right = not self.patrol_right
#                 self.patrolled_distance = 0
#
#         # Move left and right
#         if self.RIGHT:
#             self.velocity += Vector(1, 0) * self.speed
#             self.idle_frame = [0, 0]
#         if self.LEFT:
#             self.velocity += Vector(-1, 0) * self.speed
#             self.idle_frame = [2, 0]
#         self.speed = speed
#

















#     def frame_update(self):
#         if self.ATTACK1_COOLDOWN:
#             self.count += 1
#             if self.count == 30:
#                 self.ATTACK1_COOLDOWN = False
#                 self.count = 0
#
#         if self.HURT:
#             # Enable/Disable some states when hurt
#             self.LEFT, self.RIGHT, self.ATTACK1, self.ATTACK2 = False, False, False, False
#             self.JUMP, self.PATROL = False, False
#             self.ATTACK1_END = True
#
#             # Choosing correct frame
#             self.frame_index = [3, 0]
#             if self.idle_frame[0] == 0:
#                 self.frame_index = [1, 0]
#
#             # Control duration
#             if self.frame_count > 0:
#                 self.frame_count = -5
#
#             # Turn hurt off
#             if self.frame_count % 6 == 0:
#                 self.HURT = False
#
#         # Launch attack mid-air
#         elif self.ATTACK1 and (self.JUMP or self.FALL):
#             # Stops left/right movement during attack
#             self.RIGHT, self.LEFT, self.ATTACK2 = False, False, False
#             self.ATTACK1_END = False
#
#             # Choosing correct row
#             self.frame_index[1] = 8
#             if self.idle_frame == [0, 0]:
#                 self.frame_index[1] = 7
#
#             # Ensuring the column number is not greater than number of frames in the row
#             if self.frame_index[0] >= self.attack_frame:
#                 self.frame_index[0] = 0
#
#             # Reset count so animation is always played the same
#             if self.frame_count > 0:
#                 self.frame_count = -7
#
#             # Ensures player falls during midair attack
#             if self.frame_count % 8 == 0:
#                 self.JUMP = False
#                 self.FALL = True
#
#             # Control FPS of animation
#             if self.frame_count % 4 == 0:
#                 self.frame_index[0] = (self.frame_index[0] + 1) % self.attack_frame
#                 if self.frame_index[0] == 0:
#                     self.ATTACK1 = False
#                     self.ATTACK1_END = True
#
#         elif self.ATTACK2 and self.ATTACK1_END:
#             self.RIGHT, self.LEFT, self.JUMP, self.ATTACK1 = False, False, False, False
#             # Choosing correct row
#             if self.idle_frame[0] == 0:
#                 self.frame_index[1] = 9
#             elif self.frame_index[1] != 10:
#                 self.frame_index = [0, 10]
#
#             # Reset count so animation is always played the same
#             if self.frame_count > 0:
#                 self.frame_count = -6
#
#             # Control FPS
#             if self.frame_count % 7 == 0:
#                 self.frame_index[0] = (self.frame_index[0] + 1) % self.attack_frame
#
#                 # Create projectile at 4th frame
#                 if self.frame_index[0] == 3:
#                     self.SHOOTING = True
#                     self.shoot()
#
#                 # Turns off animation at last frame
#                 if self.frame_index[0] == 0:
#                     self.ATTACK2 = False
#
#         elif self.ATTACK1:
#             if not self.ATTACK1_COOLDOWN:
#                 # Stops left/right movement during attack
#                 self.RIGHT, self.LEFT, self.ATTACK2 = False, False, False
#                 self.ATTACK1_END = False
#
#                 # Choosing correct row
#                 if self.idle_frame[0] == 0:
#                     self.frame_index[1] = 5
#                 elif self.frame_index[1] != 6:
#                     self.frame_index = [0, 6]
#
#                 # Ensuring the column number is not greater than number of frames in the row
#                 if self.frame_index[0] >= self.attack_frame:
#                     self.frame_index[0] = 0
#
#                 # Reset count so animation is always played the same
#                 if self.frame_count > 0:
#                     self.frame_count = -self.fps + 1
#
#                 # Control FPS
#                 if self.frame_count % self.fps == 0:
#                     self.frame_index[0] = (self.frame_index[0] + 1) % self.attack_frame
#
#                     # Create projectile at 4th frame
#                     if self.frame_index[0] == 3 and self.player is not None:
#                         self.SHOOTING = True
#                         self.shoot()
#
#                     # Damage at 2nd frame
#                     if self.frame_index[0] == 1 and not self.is_ranged:
#                         for entity in self.game_manager.all_entities:
#                             dmg = 2
#                             target = 'enemy'
#                             if self.name == 'enemy':
#                                 dmg = 1
#                                 target = 'player'
#                             if ((entity.name == target and entity != self)
#                                     and self.game_manager.interaction_manager.is_overlapping(self, entity)):
#                                 entity.deal_damage(dmg)
#
#                     # Turns off animation at last frame
#                     if self.frame_index[0] == 0:
#                         self.ATTACK1 = False
#                         self.ATTACK1_END = True
#                         self.ATTACK1_COOLDOWN = True
#
#         elif self.JUMP:
#             self.in_jump = True
#             self.grounded = False
#             # Choosing correct row
#             self.frame_index = [0, 4]
#             if self.idle_frame == [0, 0]:
#                 self.frame_index = [0, 3]
#
#             # Reset count so animation is always played the same
#             if self.frame_count > 0:
#                 self.frame_count = -7
#
#             # Control FPS and turns off animation
#             if self.frame_count % 8 == 0:
#                 self.JUMP = False
#                 self.in_jump = False
#                 self.FALL = True
#
#         elif self.FALL:
#             # Choosing correct row
#             self.frame_index = [1, 4]
#             if self.idle_frame == [0, 0]:
#                 self.frame_index = [1, 3]
#
#             # Fall animation until touches ground
#             if self.grounded:
#                 self.FALL = False
#
#         elif self.RIGHT and not self.LEFT:
#             # Choosing correct row
#             self.frame_index[1] = 1
#             if self.frame_index[0] >= self.walk_frame:
#                 self.frame_index[0] = 0
#
#             # Control FPS
#             if self.frame_count % self.walk_frame == 0:
#                 self.frame_index[0] = (self.frame_index[0] + 1) % self.walk_frame
#
#         elif self.LEFT and not self.RIGHT:
#             # Choosing correct row
#             self.frame_index[1] = 2
#             if self.frame_index[0] >= self.walk_frame:
#                 self.frame_index[0] = 0
#
#             # Control FPS
#             if self.frame_count % self.walk_frame == 0:
#                 self.frame_index[0] = (self.frame_index[0] + 1) % self.walk_frame
#
#         else:
#             self.frame_index[0] = self.idle_frame[0]
#             self.frame_index[1] = self.idle_frame[1]
#         self.frame_count += 1
#
#     def shoot(self):
#         pass
#
#     def start_mana_recharge(self):
#         self.mana_recharge_timer.start()
#
#     def stop_mana_recharge(self):
#         if self.mana >= self.mana_max:
#             self.mana_recharge_timer.stop()
#
#     def recharge_mana(self):
#         self.mana = min(self.mana + self.mana_recharge_rate, self.mana_max)
#         self.stop_mana_recharge()
