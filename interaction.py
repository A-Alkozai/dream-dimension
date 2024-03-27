import object

class Interaction:
    def __init__(self) -> None:
        pass

    def calculate_all_collisions(self, all_entities): 
        for entity in all_entities:
            if entity.name == 'block': continue

            for entity2 in all_entities:
                if entity == entity2: continue
                # if entity2.name in entity.colission_mask: continue
                # calculate collision
                self.calculate_collisions(entity, entity2)

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
        
        #top
        if collider_left_edge <= entity.position.x <= collider_right_edge:
            # top
            if collider_top_edge <= entity_bottom_edge <= collider.position.y:
                entity.position.y = collider_top_edge - entity_radius
                # set player grounded variable
                entity.grounded = True if entity.name == 'player' else False

            # bottom
            if collider_bottom_edge >= entity_top_edge >= collider.position.y:
                entity.position.y = collider_bottom_edge + entity_radius

        if collider_top_edge <= entity.position.y <= collider_bottom_edge:
            # left
            if collider_left_edge <= entity_right_edge <= collider.position.x:
                entity.position.x = collider_left_edge - entity_radius

            # right
            if collider_right_edge >= entity_left_edge >= collider.position.x:
                entity.position.x = collider_right_edge + entity_radius

    