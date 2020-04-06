from random import randint
from calculate.distance import *


class EventFunky:
    def __init__(self, entity, **kwargs):
        self.entity = entity
        self.scare_distance = 1
        self.escape_time = 1
        self.escape_speed = kwargs["speed"]
        self.original_speed = self.entity.speed

    def spawn(self, x, y, room):
        pass

    def despawn(self):
        pass

    def speech(self, message):
        pass

    def move(self, x, y):
        pass

    def on_click(self, player):
        pass

    def arrived(self):
        pass

    def update(self, dt):
        if self.escape_time_counter > 0:
            self.escape_time_counter -= dt
        if self.escape_time_counter <= 0:
            self.entity.speed = self.original_speed
            self.escape_time_counter = 0

        if self.escape_time_counter == 0 and self.entity.room is not None:
            for player in list(self.entity.room.players.values()):
                if distance_2d(player.posX, player.posY, self.entity.posX, self.entity.posY) <= self.scare_distance:
                    self.original_speed = self.entity.speed
                    self.escape_time_counter = self.escape_time
                    self.entity.speed = self.escape_speed
                    self.escape_away(player)

    escape_time_counter = 0
    def escape_away(self, player):
        if self.entity.room is not None:
            room_content = self.entity.room.room_content
            far_accessible_positions = list(filter(
                lambda pos: distance_2d(
                    player.posX,
                    player.posY,
                    self.entity.posX,
                    self.entity.posY) < self.scare_distance+2, room_content.accessible_positions))

            if len(far_accessible_positions):
                random_point = far_accessible_positions[randint(0, len(room_content.accessible_positions)-1)]
                self.entity.move(random_point[0], random_point[1])



