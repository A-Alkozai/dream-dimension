import object


class Interaction:
    def __init__(self):
        self.player = object.player
        self.enemy_player_collision = {enemy: {player: False for player in object.players}
                                       for enemy in object.enemies}

        self.proj_character_collision = {projectile1: {entity2: False for entity2 in object.all_entities}
                                         for projectile1 in object.projectiles}

        self.proj_block_collision = {projectile2: {block2: False for block2 in object.blocks}
                                     for projectile2 in object.projectiles}

        self.proj_proj_collision = {projectile3: {projectile4: False for projectile4 in object.projectiles}
                                    for projectile3 in object.projectiles}

        self.player_on_block_collision = {player: {block1: False for block1 in object.blocks}
                                          for player in object.players}

    def reset(self):
        self.enemy_player_collision = {enemy: {player: False for player in object.players}
                                       for enemy in object.enemies}

        self.proj_character_collision = {projectile1: {entity2: False for entity2 in object.all_entities}
                                         for projectile1 in object.projectiles}

        self.proj_block_collision = {projectile2: {block2: False for block2 in object.blocks}
                                     for projectile2 in object.projectiles}

        self.proj_proj_collision = {projectile3: {projectile4: False for projectile4 in object.projectiles}
                                    for projectile3 in object.projectiles}

        self.player_on_block_collision = {player: {block1: False for block1 in object.blocks}
                                          for player in object.players}

    def update_collision(self):
        # Enemy + Player collision
        for enemy in object.enemies:
            collision_check(enemy, self.player, self.enemy_player_collision)

        # Projectile + Characters collision
        for proj in object.projectiles:
            for entity in object.all_entities:
                collision_check(proj, entity, self.proj_character_collision)

        # Projectile + Projectile collision
        for proj1 in object.projectiles:
            for proj2 in object.projectiles:
                if proj1 != proj2:
                    collision_check(proj1, proj2, self.proj_proj_collision)

        # Projectile + Block collision
        for proj in object.projectiles:
            for block in object.blocks:
                collision_check(proj, block, self.proj_block_collision, True)

        # Player + Block collision
        for block in object.blocks:
            if ((block[0] - 30 <= self.player.position.x + self.player.frame_centre_x <= block[0] + 30) or
                    (block[0] - 30 <= self.player.position.x - self.player.frame_centre_x <= block[0] + 30) and
                    (block[1] - 30 <= self.player.position.y + self.player.frame_centre_y <= block[1])):
                self.player_on_block_collision[self.player][block] = True


    def position_update(self, entity):
        for block in object.blocks:
            # Calculate the minimum and maximum x and y coordinates for the block
            min_x = block[0] - 30
            max_x = block[0] + 30
            min_y = block[1] - 30
            max_y = block[1] + 30

            if ((min_x <= entity.position.x + entity.frame_centre_x <= max_x) or
                    (min_x <= entity.position.x - entity.frame_centre_x <= max_x)):

                if min_y <= entity.position.y + entity.frame_centre_y <= block[1]:
                    entity.position.y = min_y - entity.frame_centre_y
                    print("Contact with top side of block" + str(block))

                elif block[1] <= entity.position.y - entity.frame_centre_y <= max_y:
                    entity.position.y = max_y + entity.frame_centre_y
                    print("Contact with bottom side of block" + str(block))

            if ((min_y <= entity.position.y - entity.frame_centre_y <= block[1]) or
                    (min_y <= entity.position.y + entity.frame_centre_y <= block[1])):

                if min_x <= entity.position.x + entity.frame_centre_x <= block[0]:
                    entity.position.x = min_x - entity.frame_centre_x
                    print("Contact with left side of block" + str(block))

                elif block[0] <= entity.position.x - entity.frame_centre_x <= max_x:
                    entity.position.x = max_x + entity.frame_centre_x
                    print("Contact with right side of block" + str(block))


def collision_check(entity1, entity2, dictionary, block=False):
    left1 = entity1.position.x - entity1.frame_centre_x
    right1 = entity1.position.x + entity1.frame_centre_x
    up1 = entity1.position.y - entity1.frame_centre_y
    down1 = entity1.position.y + entity1.frame_centre_y

    left2 = entity2.position.x - entity2.frame_centre_x
    right2 = entity2.position.x + entity2.frame_centre_x
    up2 = entity2.position.y - entity2.frame_centre_y
    down2 = entity2.position.y + entity2.frame_centre_y
    if block:
        left2 = entity2.position.x - 30
        right2 = entity2.position.x + 30
        up2 = entity2.position.y - 30
        down2 = entity2.position.y + 30

    if ((left2 <= right1 <= right2 or left1 <= right2 <= right1) and
            (up2 >= down1 >= down2 or up1 >= down2 >= down1)):
        dictionary[entity1][entity2] = True
