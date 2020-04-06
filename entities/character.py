import threading
import time

from calculate.a_star import a_star
from calculate.id_generator import generate_id
from calculate.distance import *
from entity_events import *


def delayed_pos_update(self, sleep_time, x, y):
    time.sleep(sleep_time/1000)
    self.posX = x
    self.posY = y

class Character:
    def __init__(self, skin):
        self.id = generate_id()
        self.spawned = False
        self.skin = skin
        self.room = None
        self.posX = 0
        self.posY = 0
        self.name = self.skin
        self.speed = 2
        self.direction = "S"
        self.type = "character"
        self.events = {}

    def get_dict(self):
        return {"id": self.id,
                "skin": self.skin,
                "x": self.posX,
                "y": self.posY,
                "type": self.type,
                "name": self.name,
                "direction": self.direction}

    def add_event(self, event_name, **kwargs):
        constructor = globals()["Event"+event_name]
        self.events[event_name] = constructor(self, **kwargs)

    def spawn(self, x, y, room):
        [event.spawn(x, y, room) for event in list(self.events.values())]
        self.posX = x
        self.posY = y
        self.last_pos_x = x
        self.last_pos_y = y
        self.move_pos_x = x
        self.move_pos_y = y
        self.room = room
        self.spawned = True
        for player in list(self.room.players.values()):
            player.client.spawn(self)

    def despawn(self):
        [event.despawn() for event in list(self.events.values())]
        self.spawned = False
        if self.room is not None:
            for player in list(self.room.players.values()):
                player.client.despawn(self)

    def speech(self, message):
        [event.speech(message) for event in list(self.events.values())]
        if self.room is not None:
            for player in list(self.room.players.values()):
                player.client.speech({"id": self.id, "message": message})

    is_moving = False
    move_pos_x = 0
    move_pos_y = 0
    last_pos_x = 0
    last_pos_y = 0
    move_path = []

    def move(self, x, y):
        [event.move(x, y) for event in list(self.events.values())]
        if self.room is not None:
            self.is_moving = True
            matrix_room_solid = self.room.room_content.matrix_solid_base
            self.move_path = a_star(matrix_room_solid, (int(self.posX), int(self.posY)), (x, y))
            if len(self.move_path):
                self.move_path.pop(0)

    def arrived(self):
        [event.arrived() for event in list(self.events.values())]

    def update(self, dt):
        [event.update(dt) for event in list(self.events.values())]
        if self.room is not None and self.spawned:
            if len(self.move_path) and self.posX == self.move_pos_x and self.posY == self.move_pos_y:
                move_pos = self.move_path.pop(0)
                self.move_pos_x = move_pos[0]
                self.move_pos_y = move_pos[1]
            elif self.is_moving and len(self.move_path) == 0 and self.posX == self.move_pos_x and self.posY == self.move_pos_y:
                self.is_moving = False
                self.arrived()
            elif self.is_moving:
                walk_distance_x = 0
                walk_distance_y = 0

                try:
                    walk_distance_x = (self.move_pos_x - self.posX) / ((abs(self.move_pos_x - self.posX) / self.speed) / dt)
                except:
                    pass
                try:
                    walk_distance_y = (self.move_pos_y - self.posY) / ((abs(self.posY - self.move_pos_y) / self.speed) / dt)
                except:
                    pass

                self.posX += walk_distance_x
                self.posY += walk_distance_y

                if walk_distance_x > 0 and self.posX > self.move_pos_x:
                    self.posX = self.move_pos_x
                if walk_distance_x < 0 and self.posX < self.move_pos_x:
                    self.posX = self.move_pos_x
                if walk_distance_y > 0 and self.posY > self.move_pos_y:
                    self.posY = self.move_pos_y
                if walk_distance_y < 0 and self.posY < self.move_pos_y:
                    self.posY = self.move_pos_y

            if self.posX != self.last_pos_x or self.posY != self.last_pos_y:
                self.last_pos_x = self.posX
                self.last_pos_y = self.posY
                for player in list(self.room.players.values()):
                    player.client.move(self.id, self.posX, self.posY, dt*1000+100)


    def on_click(self, player):
        [event.on_click(player) for event in list(self.events.values())]
        pass

