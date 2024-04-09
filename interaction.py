class Interaction:
    def __init__(self) -> None:
        pass

    def calculate_all_collisions(self, all_entities):
        for entity in all_entities:
            # Ensures blocks/ladders never collide with itself
            # Cavity, interact and special kinds do not collide with one another
            if (entity.kind == 'block' or entity.kind == 'ladder' or
                    entity.kind == 'cavity' or entity.kind == 'drop' or entity.kind == 'sfx'):
                continue

            for entity2 in all_entities:
                # Cannot collide with yourself
                if entity == entity2 or entity2.kind == 'cavity' or entity.kind == 'sfx':
                    continue
                # Calculate collisions between the 2
                self.calculate_collisions(entity, entity2)

    # Check if 2 entities are overlapping and return True/False
    def is_overlapping(self, entity, collider):
        collider_edges = self.get_collider_edges(collider)

        # Compares edges of the collider to the centre of the entity
        is_overlapping = (collider_edges['left'] < entity.position.x < collider_edges['right'] and
                          collider_edges['top'] < entity.position.y < collider_edges['bottom'])
        return is_overlapping

    # Calculates if 2 entities are colliding, and which side the collision occurred
    def is_colliding(self, entity, collider):
        # Calculating edges of collider and entity
        collider_edges = self.get_collider_edges(collider)
        entity_edges = self.get_collider_edges(entity)

        # Default: No collision detected from any direction
        in_collision = False
        collision_direction = ''
        
        # Calculate collision with top/bottom side of collider
        if collider_edges['left'] <= entity.position.x <= collider_edges['right']:
            # Top side collision
            if collider_edges['top'] <= entity_edges['bottom'] <= collider.position.y:
                in_collision = True
                collision_direction = 'top'
                
            # Bottom side collision
            if collider_edges['bottom'] >= entity_edges['top'] >= collider.position.y:
                in_collision = True
                collision_direction = 'bottom'

        # Calculate collision with left/right side of collider
        if collider_edges['top'] <= entity.position.y <= collider_edges['bottom']:
            # Left side collision
            if collider_edges['left'] <= entity_edges['right'] <= collider.position.x:
                in_collision = True
                collision_direction = 'left'
    
            # Right side collision
            if collider_edges['right'] >= entity_edges['left'] >= collider.position.x:
                in_collision = True
                collision_direction = 'right'
        # Return: True/False, the side the collision occurred at
        return in_collision, collision_direction

    # Calculate the edges of an entity
    def get_collider_edges(self, entity):
        # Almost all entities are 60x60
        entity_radius_x, entity_radius_y = 30, 30
        # Projectiles should have smaller hit-boxes
        if entity.kind == 'player_projectile' or entity.kind == 'enemy_projectile':
            entity_radius_x, entity_radius_y = 15, 15
        # These blocks have bigger hit-boxes
        elif entity.name == 'bush_floor':
            entity_radius_x, entity_radius_y = 30, 40
        # Buttons have 2 radius
        elif entity.kind == 'button':
            entity_radius_x = entity.img_dest_dim[0]/2
            entity_radius_y = entity.img_dest_dim[1]/2

        # Calculation of every edge
        collider_top_edge = entity.position.y - entity_radius_y
        collider_bottom_edge = entity.position.y + entity_radius_y
        collider_left_edge = entity.position.x - entity_radius_x
        collider_right_edge = entity.position.x + entity_radius_x

        return {
            'top': collider_top_edge,
            'bottom': collider_bottom_edge,
            'left': collider_left_edge,
            'right': collider_right_edge,
        }

    # Creates physical collision between 2 entities
    def calculate_collisions(self, entity, collider):
        entity_radius = 30
        collider_edges = self.get_collider_edges(collider)

        # Calculate if collision is occurring, and on which side
        in_collision, collision_direction = self.is_colliding(entity, collider)

        # Collision will not occur if the collider is in the collision_mask list of entity
        if collider.kind not in entity.collision_mask:
            # Moves entity away from the edge it collided with
            match collision_direction:
                case 'top': entity.position.y = collider_edges['top'] - entity_radius
                case 'bottom': entity.position.y = collider_edges['bottom'] + entity_radius
                case 'left': entity.position.x = collider_edges['left'] - entity_radius
                case 'right': entity.position.x = collider_edges['right'] + entity_radius
