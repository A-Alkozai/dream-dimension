import object

class Interaction:
    def __init__(self) -> None:
        pass

    def calculate_all_collisions(self, all_entities):
        for entity in all_entities:
            if entity.name == 'block' or entity.name == 'ladder': continue

            for entity2 in all_entities:
                if entity == entity2: continue
                # calculate collision
                self.calculate_collisions(entity, entity2)
    
    def is_overlapping(self, entity, collider):
        collider_edges = self.get_collider_edges(collider)
        is_overlapping = collider_edges['left'] < entity.position.x < collider_edges['right'] and collider_edges['top'] < entity.position.y < collider_edges['bottom']
        # print(is_overlapping)
        return is_overlapping

    def is_colliding(self, entity, collider):
         #  distance from centre of an entity to the edge
        # collider edges
        collider_edges = self.get_collider_edges(collider)

        # entity edges
        entity_edges = self.get_collider_edges(entity)

        in_collision = False
        collision_direction = ''
        
        #top
        if collider_edges['left'] <= entity.position.x <= collider_edges['right']:
            # top
            if collider_edges['top'] <= entity_edges['bottom'] <= collider.position.y:
                in_collision = True
                collision_direction = 'top'
                
            # bottom
            if collider_edges['bottom'] >= entity_edges['top'] >= collider.position.y:
                in_collision = True
                collision_direction = 'bottom'

        if collider_edges['top'] <= entity.position.y <= collider_edges['bottom']:
            # left
            if collider_edges['left'] <= entity_edges['right'] <= collider.position.x:
                in_collision = True
                collision_direction = 'left'
    
            # right
            if collider_edges['right'] >= entity_edges['left'] >= collider.position.x:
                in_collision = True
                collision_direction = 'right'

        return in_collision, collision_direction
    
    def get_collider_edges(self, entity):
        entity_radius = 30
        collider_top_edge = entity.position.y - entity_radius
        collider_bottom_edge = entity.position.y + entity_radius
        collider_left_edge = entity.position.x - entity_radius
        collider_right_edge = entity.position.x + entity_radius

        return {
            'top': collider_top_edge,
            'bottom': collider_bottom_edge,
            'left': collider_left_edge,
            'right': collider_right_edge,
        }

    def calculate_collisions(self, entity, collider):
        entity_radius = 30
        collider_edges = self.get_collider_edges(collider)
        in_collision, collision_direction = self.is_colliding(entity, collider)

        if collider.name not in entity.collision_mask:
            match collision_direction:
                case 'top': entity.position.y = collider_edges['top'] - entity_radius
                case 'bottom': entity.position.y = collider_edges['bottom'] + entity_radius
                case 'left': entity.position.x = collider_edges['left'] - entity_radius
                case 'right': entity.position.x = collider_edges['right'] + entity_radius
    
# AFK ZONE:
# >>  <<
