from random import randint


class EventRandomWalk:
    def __init__(self, entity, **kwargs):
        self.entity = entity

    def spawn(self, x, y, room):
        self.walk_cooldown = randint(3, 10)

    def despawn(self):
        pass

    def speech(self, message):
        pass

    def move(self, x, y):
        pass

    def on_click(self, player):
        pass

    def arrived(self):
        self.walk_cooldown = randint(3, 10)
        self.is_walking = False

    walk_cooldown = 0
    is_walking = False
    def update(self, dt):
        if self.walk_cooldown > 0:
            self.walk_cooldown -= dt
        elif not self.is_walking:
            self.is_walking = True
            self.random_walk()
            self.walk_cooldown = 0

    def random_walk(self):
        if self.entity.room is not None:
            room_content = self.entity.room.room_content
            random_point = room_content.accessible_positions[randint(0, len(room_content.accessible_positions)-1)]

            self.entity.move(random_point[0], random_point[1])



