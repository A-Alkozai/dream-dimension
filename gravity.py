from vector import Vector


class Gravity:
    def __init__(self, all_entities):
        self.all_entities = all_entities

    def gravity(self):
        for entity in self.all_entities:
            if entity.gravity:
                entity.velocity.y += entity.weight
