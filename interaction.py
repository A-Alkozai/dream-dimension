import object

class Interaction:
    def __init__(self) -> None:
        pass

    def calculate_all_collisions(self, all_entities):
        for entity in all_entities:
            if entity.name == 'block' or entity.name == 'ladder': continue

            for entity2 in all_entities:
                if entity == entity2: continue
                # if entity2.name in entity.collision_mask: continue
                # calculate collision
                self.calculate_collisions(entity, entity2)
    
    # def is_overlapping(self, entity, collider):
    #     return True if collider. entity.position.x

    def calculate_collisions(self, entity, collider):
        #  distance from centre of an entity to the edge
        entity_radius = 30

        # collider edges
        collider_top_edge = collider.position.y - entity_radius
        collider_bottom_edge = collider.position.y + entity_radius
        collider_left_edge = collider.position.x - entity_radius
        collider_right_edge = collider.position.x + entity_radius

        # entity edges
        entity_top_edge = entity.position.y - entity_radius
        entity_bottom_edge = entity.position.y + entity_radius
        entity_left_edge = entity.position.x - entity_radius
        entity_right_edge = entity.position.x + entity_radius

        in_collision = False
        collision_direction = ''
        
        #top
        if collider_left_edge <= entity.position.x <= collider_right_edge:
            # top
            if collider_top_edge <= entity_bottom_edge <= collider.position.y:
                in_collision = True
                collision_direction = 'top'
                
            # bottom
            if collider_bottom_edge >= entity_top_edge >= collider.position.y:
                in_collision = True
                collision_direction = 'bottom'

        if collider_top_edge <= entity.position.y <= collider_bottom_edge:
            # left
            if collider_left_edge <= entity_right_edge <= collider.position.x:
                in_collision = True
                collision_direction = 'left'
    
            # right
            if collider_right_edge >= entity_left_edge >= collider.position.x:
                in_collision = True
                collision_direction = 'right'


        if collider.name not in entity.collision_mask:
            match collision_direction:
                case 'top': entity.position.y = collider_top_edge - entity_radius
                case 'bottom': entity.position.y = collider_bottom_edge + entity_radius
                case 'left': entity.position.x = collider_left_edge - entity_radius
                case 'right': entity.position.x = collider_right_edge + entity_radius

        if in_collision:                
            # set player grounded variable
            entity.grounded = True if entity.name == 'player' else False
            entity.on_ladder = True if entity.name == 'player' and collider.name == 'ladder' else False
            if entity.name == 'player': print(entity.on_ladder)
                             
    