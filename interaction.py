import object

class Interaction:
    def __init__(self) -> None:
        pass

    def calculate_all_collisions(self, all_entities):
        for entity in all_entities:
            for entity2 in all_entities:
                if entity == entity2: continue

                # calculate collision
                self.calculate_collisions(entity, entity2)

    def calculate_colissions(entity, entity2):
        entity_radius = entity.frame_centre_x
        
        #top
        
        # if between left and right and touching/below the top but above centre

        #bottom
        # if between left and right and touching/above the bottom but below centre

        #left
        # if between top and bottom and touching/right of the left edge but left of the centre 

        #right
        # if between top and bottom and touching/left of the right edge but right of the centre 

    